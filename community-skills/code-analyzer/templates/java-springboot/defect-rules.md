# Java + SpringBoot 缺陷检测规则

## 规则概览

支持检测 8 类常见缺陷,按严重度分级:

- 🔴 **Blocker**(阻断级): SQL注入、敏感信息泄露
- 🟠 **Critical**(严重级): NPE风险、资源泄漏
- 🟡 **Major**(重要级): 事务失效、异常吞没、并发问题
- 🟢 **Minor**(次要级): 循环依赖、参数验证缺失

---

## 🔴 Blocker - 阻断级

### 1. SQL 注入

**风险等级**: 🔴 Blocker (10分)

**描述**: 使用字符串拼接构造 SQL 语句,存在 SQL 注入风险。

**危险模式**:

```java
// 模式 1: 使用 + 拼接
String sql = "SELECT * FROM user WHERE name = '" + name + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);

// 模式 2: 使用 String.format
String sql = String.format("DELETE FROM %s WHERE id = %d", table, id);

// 模式 3: 动态 ORDER BY
String orderBy = request.getParameter("orderBy");
String sql = "SELECT * FROM products ORDER BY " + orderBy;
```

**攻击示例**:

```java
// 输入: username = "admin' OR '1'='1"
// 执行: SELECT * FROM users WHERE username = 'admin' OR '1'='1'
// 结果: 绕过认证

// 输入: orderBy = "1; DROP TABLE products--"
// 执行: SELECT * FROM products ORDER BY 1; DROP TABLE products--
// 结果: 删除表
```

**检测方法**:

Level 1 - 文本匹配:

```bash
git diff HEAD~3..HEAD | grep -E '"\s*(SELECT|INSERT|UPDATE|DELETE).*(\+|String\.format)'
```

Level 2 - Serena MCP:

```
查询: "查找所有使用字符串拼接构造 SQL 的代码"
查询: "查找包含 Statement.executeQuery 且参数包含字符串拼接的代码"
```

**安全示例**:

```java
// ✅ 使用 JPA 参数化查询
@Query("SELECT u FROM User u WHERE u.name = :name")
User findByName(@Param("name") String name);

// ✅ 使用 PreparedStatement
String sql = "SELECT * FROM users WHERE username = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setString(1, username);
ResultSet rs = pstmt.executeQuery();

// ✅ 动态 ORDER BY 白名单
Set<String> allowedColumns = Set.of("name", "price", "created_at");
if (!allowedColumns.contains(orderBy)) {
    throw new IllegalArgumentException("Invalid order by column");
}
String sql = "SELECT * FROM products ORDER BY " + orderBy;
```

**修复建议**:

1. 使用 JPA `@Query` 注解 + `:name` 参数
2. 使用 `PreparedStatement` 参数绑定
3. 动态 SQL 使用白名单验证

**参考**: OWASP A03:2021 - Injection

---

### 2. 敏感信息泄露

**风险等级**: 🔴 Blocker (10分)

**描述**: 硬编码密码、密钥、Token 等敏感信息。

**危险模式**:

```java
// 模式 1: 硬编码数据库密码
String dbUrl = "jdbc:mysql://localhost:3306/db";
String dbUser = "root";
String dbPassword = "admin123";  // ❌ 硬编码密码
Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword);

// 模式 2: 硬编码 API 密钥
String apiKey = "sk_live_abc123def456";
HttpRequest request = HttpRequest.newBuilder()
    .header("Authorization", "Bearer " + apiKey)
    .build();

// 模式 3: 硬编码加密密钥
String secretKey = "mySecretKey123";
Cipher cipher = Cipher.getInstance("AES");
cipher.init(Cipher.ENCRYPT_MODE, new SecretKeySpec(secretKey.getBytes(), "AES"));
```

**检测方法**:

```bash
# 检测常见敏感字段名
git diff HEAD~3..HEAD | grep -iE '(password|apiKey|secret|token)\s*=\s*"[^"]+"'
```

Serena MCP:

```
查询: "查找所有包含 password/apiKey/secret 赋值为字符串字面量的代码"
```

**安全示例**:

```java
// ✅ 使用环境变量
String dbPassword = System.getenv("DB_PASSWORD");

// ✅ 使用 Spring 配置
@Value("${api.key}")
private String apiKey;

// application.properties
spring.datasource.password=${DB_PASSWORD}
api.key=${API_KEY}

// ✅ 使用密钥管理服务
String dbPassword = vaultClient.getSecret("db-password");
KeyStore keyStore = KeyStore.getInstance("JCEKS");
Key key = keyStore.getKey("aesKey", keyPassword);
```

**修复建议**:

1. 使用环境变量或配置文件(不提交到 Git)
2. 使用密钥管理服务(Vault, AWS Secrets Manager)
3. 在 `.gitignore` 中排除配置文件

**参考**: OWASP A02:2021 - Cryptographic Failures

---

## 🟠 Critical - 严重级

### 3. NPE (NullPointerException) 风险

**风险等级**: 🟠 Critical (5分)

**描述**: 方法调用前未检查 null,可能导致运行时 NPE。

**危险模式**:

```java
// 模式 1: Repository 查询结果未检查
User user = userRepository.findById(id);  // 可能返回 null
user.getName();  // ❌ NPE

// 模式 2: Optional 直接 get()
User user = userRepository.findById(id).get();  // ❌ 未检查 isPresent()

// 模式 3: Map.get() 未检查
String value = map.get(key);
value.toUpperCase();  // ❌ NPE

// 模式 4: 集合操作未检查空
List<String> list = getList();
String first = list.get(0);  // ❌ list 可能为 null 或空

// 模式 5: 方法参数未验证
public void process(User user) {
    user.getName();  // ❌ 未验证 user 是否为 null
}
```

**检测方法**:

Serena MCP:

```
查询: "查找所有调用 findById 但未检查返回值是否为 null 的代码"
查询: "查找所有调用 Optional.get() 但未先调用 isPresent() 的代码"
查询: "查找所有调用 Map.get() 后直接调用方法的代码"
```

**安全示例**:

```java
// ✅ 检查后使用
User user = userRepository.findById(id);
if (user == null) {
    throw new NotFoundException("用户不存在");
}
user.getName();

// ✅ Optional.orElseThrow
User user = userRepository.findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));

// ✅ Optional 链式调用
return userRepository.findById(id)
    .map(User::getName)
    .orElse("Unknown");

// ✅ 集合检查
List<String> list = getList();
if (list != null && !list.isEmpty()) {
    String first = list.get(0);
}

// ✅ 参数验证
public void process(User user) {
    Objects.requireNonNull(user, "user cannot be null");
    user.getName();
}
```

**修复建议**:

1. 使用 `Optional` API (`orElseThrow`, `map`, `orElse`)
2. 添加 null 检查或使用 `Objects.requireNonNull()`
3. 使用 `@NonNull` 注解 (Lombok/Jakarta Validation)

---

### 4. 资源泄漏

**风险等级**: 🟠 Critical (5分)

**描述**: 数据库连接、文件流、HTTP 客户端等资源未正确关闭。

**危险模式**:

```java
// 模式 1: 数据库连接未关闭
Connection conn = dataSource.getConnection();
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(sql);
// ❌ 未关闭资源 → 连接池耗尽

// 模式 2: 文件流未关闭
FileInputStream fis = new FileInputStream("file.txt");
// ❌ 未关闭 → 文件句柄泄漏

// 模式 3: HTTP 客户端未关闭
CloseableHttpClient client = HttpClients.createDefault();
HttpResponse response = client.execute(request);
// ❌ 未关闭 → 线程泄漏
```

**检测方法**:

```bash
# 检测创建但未关闭的资源
git diff HEAD~3..HEAD | grep -E '(Connection|InputStream|OutputStream|HttpClient)\s+\w+\s*=' | \
  grep -v 'try-with-resources'
```

Serena MCP:

```
查询: "查找所有创建 Connection/Stream/HttpClient 但未使用 try-with-resources 的代码"
```

**安全示例**:

```java
// ✅ 使用 try-with-resources (Java 7+)
try (Connection conn = dataSource.getConnection();
     Statement stmt = conn.createStatement();
     ResultSet rs = stmt.executeQuery(sql)) {

    while (rs.next()) {
        // 处理数据
    }
} // 自动关闭所有资源

// ✅ 文件操作
try (FileInputStream fis = new FileInputStream("file.txt")) {
    // 读取文件
}

// ✅ 使用 NIO Files (推荐)
List<String> lines = Files.readAllLines(Paths.get("file.txt"));

// ✅ HTTP 客户端
try (CloseableHttpClient client = HttpClients.createDefault()) {
    HttpResponse response = client.execute(request);
}
```

**修复建议**:

1. 使用 `try-with-resources` 自动管理资源
2. 使用高级 API (NIO Files, Spring RestTemplate)
3. 确保 finally 块中关闭资源(不推荐,易出错)

---

## 🟡 Major - 重要级

### 5. 事务失效

**风险等级**: 🟡 Major (2分)

**描述**: `@Transactional` 注解使用不当,事务未生效。

**危险模式**:

```java
// 模式 1: 同类内部调用
@Service
public class UserService {
    public void updateUser(User user) {
        userRepository.save(user);
        sendEmail(user);  // ❌ 同类调用,@Transactional 不生效
    }

    @Transactional
    public void sendEmail(User user) {
        // 事务未生效
    }
}

// 模式 2: 方法不是 public
@Transactional
private void updateUser(User user) {  // ❌ private 方法事务不生效
    userRepository.save(user);
}

// 模式 3: 异常被捕获未抛出
@Transactional
public void transfer(Long fromId, Long toId, BigDecimal amount) {
    try {
        accountService.deduct(fromId, amount);
        accountService.add(toId, amount);
    } catch (Exception e) {
        e.printStackTrace();  // ❌ 异常被吞没,事务不回滚
    }
}
```

**检测方法**:

Serena MCP:

```
查询: "查找所有 @Transactional 方法但方法可见性不是 public 的代码"
查询: "查找所有在同一个类中调用 @Transactional 方法的代码"
查询: "查找所有 @Transactional 方法内部捕获异常但未重新抛出的代码"
```

**安全示例**:

```java
// ✅ 拆分到不同 Service
@Service
public class UserService {
    @Autowired
    private EmailService emailService;

    @Transactional
    public void updateUser(User user) {
        userRepository.save(user);
        emailService.sendEmail(user);  // 跨类调用,事务生效
    }
}

// ✅ 注入自身代理
@Service
public class UserService {
    @Autowired
    private UserService self;  // 注入自身

    public void updateUser(User user) {
        userRepository.save(user);
        self.sendEmail(user);  // 通过代理调用
    }

    @Transactional
    public void sendEmail(User user) {
        // 事务生效
    }
}

// ✅ 异常重新抛出
@Transactional
public void transfer(Long fromId, Long toId, BigDecimal amount) {
    try {
        accountService.deduct(fromId, amount);
        accountService.add(toId, amount);
    } catch (Exception e) {
        log.error("Transfer failed", e);
        throw e;  // 重新抛出,触发回滚
    }
}
```

**修复建议**:

1. 拆分到不同 Service 或注入自身代理
2. 确保方法是 `public`
3. 异常必须重新抛出或使用 `@Transactional(rollbackFor = Exception.class)`

---

### 6. 异常吞没

**风险等级**: 🟡 Major (2分)

**描述**: catch 块捕获异常后仅打印日志,未处理或重新抛出。

**危险模式**:

```java
// 模式 1: 空 catch 块
try {
    processOrder(order);
} catch (Exception e) {
    // ❌ 完全吞没异常
}

// 模式 2: 仅打印日志
try {
    paymentService.pay(amount);
} catch (Exception e) {
    e.printStackTrace();  // ❌ 仅打印,未处理
}

// 模式 3: 记录日志但未回滚
@Transactional
public void createOrder(Order order) {
    try {
        orderRepository.save(order);
        inventoryService.deduct(order.getItems());
    } catch (Exception e) {
        log.error("Order creation failed", e);  // ❌ 事务不回滚
    }
}
```

**检测方法**:

```bash
git diff HEAD~3..HEAD | grep -A3 "catch\s*(" | grep -E "(printStackTrace|^$)"
```

Serena MCP:

```
查询: "查找所有 catch 块只包含 printStackTrace 或为空的代码"
```

**安全示例**:

```java
// ✅ 重新抛出
try {
    processOrder(order);
} catch (OrderException e) {
    log.error("Order processing failed: {}", order.getId(), e);
    throw e;
}

// ✅ 包装后抛出
try {
    paymentService.pay(amount);
} catch (PaymentException e) {
    throw new BusinessException("支付失败", e);
}

// ✅ 事务回滚
@Transactional
public void createOrder(Order order) {
    try {
        orderRepository.save(order);
        inventoryService.deduct(order.getItems());
    } catch (Exception e) {
        log.error("Order creation failed", e);
        throw new OrderCreationException("订单创建失败", e);  // 触发回滚
    }
}
```

**修复建议**:

1. 重新抛出异常或包装为业务异常
2. 在事务方法中必须抛出异常以触发回滚
3. 如果确实需要吞没,添加明确注释说明原因

---

### 7. 并发问题

**风险等级**: 🟡 Major (2分)

**描述**: 多线程环境下的竞态条件、非线程安全集合。

**危险模式**:

```java
// 模式 1: 竞态条件
class Counter {
    private int count = 0;

    public void increment() {
        count++;  // ❌ 非原子操作
    }
}

// 模式 2: 双重检查锁未使用 volatile
class Singleton {
    private static Singleton instance;  // ❌ 未使用 volatile

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// 模式 3: 非线程安全集合
class Cache {
    private Map<String, Object> cache = new HashMap<>();  // ❌ 多线程不安全

    public void put(String key, Object value) {
        cache.put(key, value);
    }
}
```

**检测方法**:

Serena MCP:

```
查询: "查找所有使用 HashMap 但可能在多线程环境访问的代码"
查询: "查找所有双重检查锁但变量未使用 volatile 的代码"
```

**安全示例**:

```java
// ✅ 使用 AtomicInteger
class Counter {
    private AtomicInteger count = new AtomicInteger(0);

    public void increment() {
        count.incrementAndGet();
    }
}

// ✅ 添加 volatile
class Singleton {
    private static volatile Singleton instance;

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// ✅ 使用静态内部类 (更好)
class Singleton {
    private static class Holder {
        private static final Singleton INSTANCE = new Singleton();
    }

    public static Singleton getInstance() {
        return Holder.INSTANCE;
    }
}

// ✅ 使用 ConcurrentHashMap
class Cache {
    private Map<String, Object> cache = new ConcurrentHashMap<>();

    public void put(String key, Object value) {
        cache.put(key, value);
    }
}
```

**修复建议**:

1. 使用 `java.util.concurrent` 包下的线程安全类
2. 双重检查锁必须使用 `volatile`
3. 优先使用静态内部类实现单例

---

## 🟢 Minor - 次要级

### 8. N+1 查询问题

**风险等级**: 🟢 Minor (1分) - 性能问题,不影响功能

**描述**: 循环中执行数据库查询,导致性能问题。

**危险模式**:

```java
// 模式 1: 循环查询
List<Order> orders = orderRepository.findAll();
for (Order order : orders) {
    User user = userRepository.findById(order.getUserId());  // ❌ N+1
    order.setUser(user);
}

// 模式 2: JPA 关联懒加载
@Entity
public class Order {
    @ManyToOne(fetch = FetchType.LAZY)
    private User user;
}

List<Order> orders = orderRepository.findAll();
for (Order order : orders) {
    order.getUser().getName();  // ❌ 触发 N 次查询
}
```

**检测方法**:

Level 1:

```bash
git diff HEAD~3..HEAD | grep -E 'for.*\{' -A10 | grep 'Repository.*find'
```

Level 2 - Serena MCP:

```
查询: "查找所有在循环内调用 Repository.findById 或 find 方法的代码"
```

**安全示例**:

```java
// ✅ 批量查询
List<Order> orders = orderRepository.findAll();
List<Long> userIds = orders.stream()
    .map(Order::getUserId)
    .collect(Collectors.toList());

Map<Long, User> userMap = userRepository.findAllById(userIds).stream()
    .collect(Collectors.toMap(User::getId, user -> user));

orders.forEach(order -> order.setUser(userMap.get(order.getUserId())));

// ✅ JPA 使用 @EntityGraph
@EntityGraph(attributePaths = {"user"})
List<Order> findAllWithUser();

// ✅ 使用 JOIN FETCH
@Query("SELECT o FROM Order o JOIN FETCH o.user")
List<Order> findAllWithUser();
```

**修复建议**:

1. 使用 `findAllById()` 批量查询
2. 使用 JPA `@EntityGraph` 或 `JOIN FETCH`
3. 使用 Map 缓存查询结果

---

## 功能缺陷检测

除了上述代码质量缺陷,还需要验证需求实现情况:

### 功能完全缺失 (CRITICAL)

需求明确要求的功能在代码中完全找不到。

**识别方法**:

1. 提取需求中的关键操作动词 (记录、发送、验证、生成等)
2. 在代码变更中搜索对应的方法名、类名、注释
3. 未找到任何匹配项 → 功能缺失

**示例**:

需求: "用户登录成功后,系统需要记录登录日志"

```java
// ❌ 缺失日志记录功能
@PostMapping("/login")
public ResponseEntity<UserVO> login(@RequestBody LoginRequest request) {
    User user = authService.authenticate(request);
    return ResponseEntity.ok(userMapper.toVO(user));
}
```

### 功能实现不完整 (HIGH)

功能部分实现,但缺少关键逻辑分支或边界条件处理。

**示例**:

需求: "支持手机号和邮箱两种登录方式"

```java
// ❌ 只实现了手机号登录
public User login(String username, String credential) {
    if (isPhoneNumber(username)) {
        return phoneLoginService.verify(username, credential);
    }
    // 缺少邮箱登录分支
    throw new UnsupportedOperationException("Unsupported login method");
}
```

### 业务逻辑错误 (CRITICAL)

代码实现与需求描述的业务流程矛盾。

**示例**:

需求: "支付流程: 1.验证余额 2.扣减余额 3.创建支付记录"

```java
// ❌ 流程顺序错误
public Payment pay(Long userId, BigDecimal amount) {
    accountService.deduct(userId, amount);  // 先扣款
    if (accountService.getBalance(userId).compareTo(amount) < 0) {  // 后验证
        throw new InsufficientBalanceException();
    }
    return paymentService.create(userId, amount);
}
```

---

## 检测优先级汇总

| 缺陷类型 | 严重程度 | 分数 | 影响 | 检测关键词 |
|---------|---------|------|------|-----------|
| SQL 注入 | 🔴 Blocker | 10 | 数据泄露 | SQL + string concatenation |
| 敏感信息泄露 | 🔴 Blocker | 10 | 凭证泄露 | password/key = "..." |
| NPE 风险 | 🟠 Critical | 5 | 服务中断 | null without check |
| 资源泄漏 | 🟠 Critical | 5 | 资源耗尽 | Connection without close |
| 事务失效 | 🟡 Major | 2 | 数据不一致 | @Transactional misuse |
| 异常吞没 | 🟡 Major | 2 | 隐藏错误 | Empty catch / printStackTrace |
| 并发问题 | 🟡 Major | 2 | 数据不一致 | Non-thread-safe collections |
| N+1 查询 | 🟢 Minor | 1 | 性能下降 | Loop + Repository.find |

**风险分数计算**: `Blocker×10 + Critical×5 + Major×2 + Minor×1`

---

## 参考资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Effective Java (3rd Edition)](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)
- [Java Concurrency in Practice](https://jcip.net/)
- [SpotBugs](https://spotbugs.github.io/)
- [SonarQube Java Rules](https://rules.sonarsource.com/java/)

---

**版本**: 1.0.0
**创建**: 2025-10-27
