// TDD 示例：User Service 性能优化测试
const { UserService } = require('../src/user-service');
const { performance } = require('perf_hooks');

describe('UserService Performance Tests', () => {
  let userService;
  
  beforeEach(() => {
    userService = new UserService();
  });

  // 性能基准测试
  describe('响应时间基准', () => {
    test('getUserById 应该在100ms内完成', async () => {
      const startTime = performance.now();
      
      await userService.getUserById(1);
      
      const endTime = performance.now();
      const responseTime = endTime - startTime;
      
      expect(responseTime).toBeLessThan(100); // 100ms基准
    });

    test('批量查询用户应该使用缓存优化', async () => {
      const userIds = [1, 2, 3, 4, 5];
      const startTime = performance.now();
      
      // 第一次查询 - 建立缓存
      await userService.getMultipleUsers(userIds);
      
      const cacheTime = performance.now();
      
      // 第二次查询 - 使用缓存
      await userService.getMultipleUsers(userIds);
      
      const endTime = performance.now();
      
      const firstQueryTime = cacheTime - startTime;
      const cachedQueryTime = endTime - cacheTime;
      
      // 缓存查询应该比首次查询快至少50%
      expect(cachedQueryTime).toBeLessThan(firstQueryTime * 0.5);
    });
  });

  // 并发安全测试
  describe('并发处理能力', () => {
    test('应该支持100个并发用户查询', async () => {
      const promises = [];
      
      // 创建100个并发请求
      for (let i = 1; i <= 100; i++) {
        promises.push(userService.getUserById(i % 10)); // 重复查询以测试缓存
      }
      
      const startTime = performance.now();
      const results = await Promise.all(promises);
      const endTime = performance.now();
      
      // 所有请求都应该成功
      expect(results).toHaveLength(100);
      results.forEach(result => {
        expect(result).toBeDefined();
        expect(result.id).toBeDefined();
      });
      
      // 总处理时间应该在合理范围内
      expect(endTime - startTime).toBeLessThan(1000); // 1秒内完成100个查询
    });
  });

  // 错误处理测试
  describe('容错能力', () => {
    test('数据库连接失败时应该返回缓存数据', async () => {
      // 先建立缓存
      await userService.getUserById(1);
      
      // 模拟数据库故障
      userService.simulateDatabaseFailure(true);
      
      // 应该从缓存返回数据
      const user = await userService.getUserById(1);
      expect(user).toBeDefined();
      expect(user.source).toBe('cache');
    });

    test('无效用户ID应该优雅处理', async () => {
      await expect(userService.getUserById(-1)).rejects.toThrow('Invalid user ID');
      await expect(userService.getUserById('invalid')).rejects.toThrow('Invalid user ID');
      await expect(userService.getUserById(null)).rejects.toThrow('Invalid user ID');
    });
  });
});

// 压力测试
describe('UserService Stress Tests', () => {
  test('内存使用应该稳定', async () => {
    const initialMemory = process.memoryUsage().heapUsed;
    
    // 执行大量操作
    for (let i = 0; i < 1000; i++) {
      await userService.getUserById(i % 100);
    }
    
    const finalMemory = process.memoryUsage().heapUsed;
    const memoryIncrease = finalMemory - initialMemory;
    
    // 内存增长应该控制在合理范围内 (10MB)
    expect(memoryIncrease).toBeLessThan(10 * 1024 * 1024);
  });
});