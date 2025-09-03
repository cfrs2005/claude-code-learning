// 包含多种安全问题的代码示例
const express = require('express');
const mysql = require('mysql');
const app = express();

// 问题1: 硬编码的数据库凭据
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: 'admin123',  // 硬编码密码
    database: 'production_db'
};

const connection = mysql.createConnection(dbConfig);

// 问题2: SQL 注入漏洞
app.get('/user', (req, res) => {
    const userId = req.query.id;
    // 直接拼接 SQL，存在注入风险
    const query = `SELECT * FROM users WHERE id = ${userId}`;
    
    connection.query(query, (err, results) => {
        if (err) {
            // 问题3: 错误信息泄露
            res.status(500).send(`Database error: ${err.message}`);
            return;
        }
        res.json(results);
    });
});

// 问题4: XSS 漏洞
app.get('/search', (req, res) => {
    const searchTerm = req.query.q;
    // 直接输出用户输入，存在 XSS 风险
    res.send(`<h1>搜索结果: ${searchTerm}</h1>`);
});

// 问题5: 缺少权限验证
app.delete('/admin/users/:id', (req, res) => {
    const userId = req.params.id;
    // 没有验证用户是否有管理员权限
    const deleteQuery = `DELETE FROM users WHERE id = ${userId}`;
    
    connection.query(deleteQuery, (err, results) => {
        if (err) {
            res.status(500).send('删除失败');
            return;
        }
        res.send('用户已删除');
    });
});

// 问题6: 敏感信息记录
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    
    // 问题: 在日志中记录明文密码
    console.log(`Login attempt: ${username}/${password}`);
    
    const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`;
    
    connection.query(query, (err, results) => {
        if (err || results.length === 0) {
            res.status(401).send('登录失败');
            return;
        }
        
        // 问题7: 在响应中返回敏感信息
        res.json({
            success: true,
            user: results[0]  // 可能包含密码哈希等敏感数据
        });
    });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});