// TDD 实现：User Service 优化版本
const Redis = require('redis');
const { Pool } = require('pg');

class UserService {
  constructor() {
    // 数据库连接池
    this.dbPool = new Pool({
      host: process.env.DB_HOST || 'localhost',
      user: process.env.DB_USER || 'postgres', 
      password: process.env.DB_PASSWORD || 'password',
      database: process.env.DB_NAME || 'userdb',
      max: 20, // 连接池大小
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });

    // Redis 缓存
    this.cache = Redis.createClient({
      host: process.env.REDIS_HOST || 'localhost',
      port: process.env.REDIS_PORT || 6379,
    });

    this.cache.connect();
    
    // 故障模拟标志（用于测试）
    this.databaseFailure = false;
  }

  async getUserById(userId) {
    // 输入验证
    if (!userId || userId <= 0 || typeof userId !== 'number') {
      throw new Error('Invalid user ID');
    }

    const cacheKey = `user:${userId}`;

    try {
      // 1. 先检查缓存
      const cachedUser = await this.cache.get(cacheKey);
      if (cachedUser) {
        const user = JSON.parse(cachedUser);
        user.source = 'cache';
        return user;
      }

      // 2. 模拟数据库故障（测试用）
      if (this.databaseFailure) {
        throw new Error('Database connection failed');
      }

      // 3. 从数据库查询
      const query = 'SELECT id, name, email, created_at FROM users WHERE id = $1';
      const startTime = performance.now();
      
      const result = await this.dbPool.query(query, [userId]);
      
      const queryTime = performance.now() - startTime;
      
      if (result.rows.length === 0) {
        return null;
      }

      const user = result.rows[0];
      user.source = 'database';
      user.queryTime = queryTime;

      // 4. 存入缓存（TTL 5分钟）
      await this.cache.setEx(cacheKey, 300, JSON.stringify(user));

      return user;

    } catch (error) {
      // 容错：尝试从缓存获取过期数据
      if (error.message.includes('Database connection failed')) {
        const staleUser = await this.cache.get(cacheKey);
        if (staleUser) {
          const user = JSON.parse(staleUser);
          user.source = 'cache';
          user.stale = true;
          return user;
        }
      }
      throw error;
    }
  }

  async getMultipleUsers(userIds) {
    // 输入验证
    if (!Array.isArray(userIds) || userIds.length === 0) {
      throw new Error('Invalid user IDs array');
    }

    const results = [];
    const uncachedIds = [];

    // 批量检查缓存
    for (const userId of userIds) {
      const cacheKey = `user:${userId}`;
      try {
        const cachedUser = await this.cache.get(cacheKey);
        if (cachedUser) {
          const user = JSON.parse(cachedUser);
          user.source = 'cache';
          results.push(user);
        } else {
          uncachedIds.push(userId);
        }
      } catch (error) {
        uncachedIds.push(userId);
      }
    }

    // 批量查询未缓存的用户
    if (uncachedIds.length > 0) {
      const placeholders = uncachedIds.map((_, index) => `$${index + 1}`).join(',');
      const query = `SELECT id, name, email, created_at FROM users WHERE id IN (${placeholders})`;
      
      try {
        const dbResult = await this.dbPool.query(query, uncachedIds);
        
        for (const user of dbResult.rows) {
          user.source = 'database';
          results.push(user);
          
          // 存入缓存
          const cacheKey = `user:${user.id}`;
          await this.cache.setEx(cacheKey, 300, JSON.stringify(user));
        }
      } catch (error) {
        console.error('Database query failed:', error);
        // 在生产环境中，这里可以返回部分结果或降级处理
      }
    }

    // 按原始顺序排序
    const sortedResults = userIds.map(id => 
      results.find(user => user.id === id)
    ).filter(user => user !== undefined);

    return sortedResults;
  }

  // 健康检查
  async healthCheck() {
    const health = {
      database: 'unknown',
      cache: 'unknown',
      timestamp: Date.now()
    };

    try {
      // 检查数据库连接
      await this.dbPool.query('SELECT 1');
      health.database = 'healthy';
    } catch (error) {
      health.database = 'unhealthy';
      health.databaseError = error.message;
    }

    try {
      // 检查缓存连接
      await this.cache.ping();
      health.cache = 'healthy';
    } catch (error) {
      health.cache = 'unhealthy';
      health.cacheError = error.message;
    }

    return health;
  }

  // 缓存统计
  async getCacheStats() {
    try {
      const info = await this.cache.info('memory');
      return {
        memory: info,
        keyCount: await this.cache.dbSize()
      };
    } catch (error) {
      return { error: error.message };
    }
  }

  // 清除缓存
  async clearCache(pattern = 'user:*') {
    try {
      const keys = await this.cache.keys(pattern);
      if (keys.length > 0) {
        await this.cache.del(keys);
      }
      return keys.length;
    } catch (error) {
      throw new Error(`Failed to clear cache: ${error.message}`);
    }
  }

  // 测试工具：模拟数据库故障
  simulateDatabaseFailure(enabled) {
    this.databaseFailure = enabled;
  }

  // 优雅关闭
  async shutdown() {
    await this.dbPool.end();
    await this.cache.quit();
  }
}

module.exports = { UserService };