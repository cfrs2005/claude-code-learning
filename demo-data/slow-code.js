// 性能问题代码示例
class UserService {
    constructor() {
        this.users = [];
        this.cache = new Map();
    }

    // 问题1: O(n²) 的嵌套循环
    findUsersByRole(targetRole) {
        const result = [];
        for (let i = 0; i < this.users.length; i++) {
            for (let j = 0; j < this.users[i].roles.length; j++) {
                if (this.users[i].roles[j] === targetRole) {
                    result.push(this.users[i]);
                    break;
                }
            }
        }
        return result;
    }

    // 问题2: 频繁的数据库查询
    async getUsersWithDetails(userIds) {
        const users = [];
        for (const id of userIds) {
            // 每个用户都单独查询数据库 - N+1 问题
            const user = await this.database.findById(id);
            const profile = await this.database.getProfile(id);
            const permissions = await this.database.getPermissions(id);
            users.push({ ...user, profile, permissions });
        }
        return users;
    }

    // 问题3: 内存泄漏风险
    addUserToCache(user) {
        // 缓存无限制增长
        this.cache.set(user.id, {
            ...user,
            timestamp: Date.now(),
            largeData: new Array(10000).fill(user.data) // 不必要的大数据
        });
    }

    // 问题4: 同步阻塞操作
    processLargeDataset(data) {
        let result = [];
        // 大量计算阻塞主线程
        for (let i = 0; i < data.length; i++) {
            for (let j = 0; j < data[i].length; j++) {
                result.push(this.expensiveCalculation(data[i][j]));
            }
        }
        return result;
    }

    expensiveCalculation(item) {
        // 模拟复杂计算
        let sum = 0;
        for (let i = 0; i < 100000; i++) {
            sum += Math.sqrt(item * i);
        }
        return sum;
    }
}