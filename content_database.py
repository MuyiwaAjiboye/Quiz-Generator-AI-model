COMPUTING_CONTENT = {
    "python": """
            Python is a versatile, high-level programming language known for its readability and extensive ecosystem. Its design philosophy emphasizes code readability through significant whitespace and clear syntax.

            Core Python Concepts:

            Variables and Data Types:
            - Dynamic typing allows variable type changes
            - Basic types: int, float, str, bool
            - Complex types: list, tuple, dict, set
            Example type handling:
            x = 5           # int
            x = "Hello"     # now a str
            x = [1, 2, 3]   # now a list
            print(type(x))  # prints: <class 'list'>

            Control Flow Structures:

            Conditional Statements:
            if condition:
                # code block
            elif another_condition:
                # code block
            else:
                # code block

            Loops:
            for item in iterable:
                # process item

            while condition:
                # code block
                if break_condition:
                    break
                if skip_condition:
                    continue

            Functions and Parameters:
            def greet(name, greeting="Hello"):    # Default parameter
                return f"{greeting}, {name}!"

            # Args and kwargs
            def flexible_function(*args, **kwargs):
                for arg in args:
                    print(arg)
                for key, value in kwargs.items():
                    print(f"{key}: {value}")

            Object-Oriented Programming:

            Class Definition:
            class BankAccount:
                def __init__(self, owner, balance=0):
                    self.owner = owner
                    self._balance = balance    # Protected attribute

                @property
                def balance(self):
                    return self._balance

                def deposit(self, amount):
                    if amount > 0:
                        self._balance += amount
                        return True
                    return False

            Inheritance and Polymorphism:
            class SavingsAccount(BankAccount):
                def __init__(self, owner, balance=0, interest_rate=0.01):
                    super().__init__(owner, balance)
                    self.interest_rate = interest_rate

                def apply_interest(self):
                    interest = self._balance * self.interest_rate
                    self.deposit(interest)

            Advanced Python Features:

            List Comprehensions:
            # Traditional loop
            squares = []
            for x in range(10):
                squares.append(x**2)

            # List comprehension
            squares = [x**2 for x in range(10)]

            # With condition
            even_squares = [x**2 for x in range(10) if x % 2 == 0]

            Decorators:
            def timer(func):
                def wrapper(*args, **kwargs):
                    start = time.time()
                    result = func(*args, **kwargs)
                    end = time.time()
                    print(f"{func.__name__} took {end-start} seconds")
                    return result
                return wrapper

            @timer
            def slow_function():
                time.sleep(1)

            Context Managers:
            class FileManager:
                def __init__(self, filename, mode):
                    self.filename = filename
                    self.mode = mode
                    self.file = None

                def __enter__(self):
                    self.file = open(self.filename, self.mode)
                    return self.file

                def __exit__(self, exc_type, exc_val, exc_tb):
                    if self.file:
                        self.file.close()

            Generators and Iterators:
            def fibonacci(n):
                a, b = 0, 1
                for _ in range(n):
                    yield a
                    a, b = b, a + b

            Exception Handling:
            try:
                result = risky_operation()
            except ValueError as e:
                print(f"Value error: {e}")
            except (TypeError, KeyError) as e:
                print(f"Type or Key error: {e}")
            else:
                print("Operation succeeded")
            finally:
                cleanup_resources()
        """,
    "data_structures": """
            Data Structures form the fundamental building blocks of computer science and software development. They provide organized ways to store and manage data efficiently, directly impacting program performance and resource utilization.

            Arrays and Lists represent the most basic form of data organization. An array is a collection of elements stored in contiguous memory locations, making it incredibly efficient for accessing elements using their index positions. When you access an element in an array using its index, the operation happens in constant time O(1) because the computer can directly calculate the memory address of that element. However, arrays come with limitations - their size is typically fixed at creation time, and inserting or deleting elements can be expensive as it might require shifting many elements.

            Lists, particularly dynamic lists or ArrayLists, evolved to address these limitations. They provide the same direct access benefits of arrays but can grow or shrink as needed. Behind the scenes, when a dynamic list fills up, it typically creates a new, larger array (usually double the size) and copies all elements over. While this seems expensive, the amortized cost of insertions remains O(1), making dynamic lists very practical for many applications.

            Linked Lists introduce a completely different approach to organizing data. Instead of storing elements in contiguous memory, each element (node) contains both data and a reference (or link) to the next element. This structure offers remarkable flexibility - inserting or deleting elements simply requires updating these references, which is a constant time O(1) operation when you have a reference to the relevant position. The trade-off is that accessing elements requires traversing the list from the beginning, resulting in O(n) time complexity for access operations.

            Consider a real-world analogy: Arrays are like numbered seats in a theater - finding a specific seat number is easy, but adding a new seat in the middle requires moving all subsequent seats. Linked Lists are more like a treasure hunt, where each clue points to the next location - following the trail takes time, but adding a new clue only requires updating two references.

            Trees represent a hierarchical organization of data, similar to family trees or organizational charts. Binary Search Trees (BST) are particularly powerful because they maintain their elements in a sorted order while allowing for efficient operations. In a BST, each node has at most two children, with all left descendants having smaller values and all right descendants having larger values than the node itself. This organization enables efficient searching - at each node, you can eliminate half of the remaining elements from consideration, leading to O(log n) time complexity for search, insert, and delete operations in balanced trees.

            However, BSTs can become unbalanced, potentially degrading to O(n) performance. This led to the development of self-balancing trees like AVL Trees and Red-Black Trees. These structures automatically maintain their balance through rotations after insertions and deletions, ensuring consistent O(log n) performance.

            Hash Tables combine the best of both worlds - array-like access speed with dynamic size management. They achieve this through a hash function that converts keys into array indices. A good hash function distributes elements uniformly across the available space, enabling O(1) average case performance for insertions, deletions, and lookups. However, hash collisions (when different keys hash to the same index) must be handled properly, typically through chaining (creating linked lists at each index) or open addressing (finding the next available slot).

            Understanding hash tables is crucial as they form the backbone of many practical applications:
            - Database indexing uses hash tables for quick record lookup
            - Programming language implementations use hash tables for symbol tables
            - Caching systems rely on hash tables for fast data retrieval
            - Spell checkers use hash tables to store dictionaries

            Graphs represent perhaps the most flexible data structure, capable of modeling complex relationships between entities. A graph consists of vertices (nodes) connected by edges, which can be directed (one-way) or undirected (two-way). They can represent anything from social networks (where vertices are people and edges are friendships) to computer networks (where vertices are devices and edges are connections) to map applications (where vertices are locations and edges are roads).

            The two main ways to represent graphs are:
            1. Adjacency Matrices: A 2D array where element [i][j] indicates if there's an edge from vertex i to vertex j. This representation provides O(1) edge lookup but requires O(V²) space, where V is the number of vertices.
            2. Adjacency Lists: Each vertex maintains a list of its neighboring vertices. This approach is more space-efficient for sparse graphs and makes it easier to find all neighbors of a vertex.

            The choice between these representations depends on the graph's density and the types of operations needed. Dense graphs (many edges) might benefit from adjacency matrices, while sparse graphs are better served by adjacency lists.
        """,

        "algorithms": """
            Algorithms represent the heart of computer science, providing systematic approaches to solving computational problems. Understanding algorithms isn't just about knowing their steps - it's about comprehending their efficiency, applicability, and trade-offs in different scenarios.

            Sorting algorithms demonstrate fundamental algorithmic concepts and trade-offs beautifully. Bubble Sort, while inefficient with its O(n²) time complexity, illustrates basic algorithm design through its simple approach of repeatedly stepping through the list, comparing adjacent elements and swapping them if they're in the wrong order. This algorithm gets its name from the way larger elements "bubble up" to their correct positions.

            The inefficiency of Bubble Sort becomes apparent when dealing with larger datasets, leading to the development of more sophisticated approaches. Merge Sort, for instance, employs a divide-and-conquer strategy. It splits the array into smaller subarrays, sorts them independently, and then merges these sorted subarrays. This approach guarantees O(n log n) time complexity regardless of the input data's initial order. However, it requires additional O(n) space for merging, illustrating an important space-time trade-off.

            Quick Sort, often considered the most practical general-purpose sorting algorithm, also uses divide-and-conquer but with a different approach. It selects a 'pivot' element and partitions the array around it, placing smaller elements before and larger elements after. While its worst-case time complexity is O(n²), its average case performance of O(n log n) and in-place operation make it highly efficient in practice. The choice of pivot selection strategy significantly impacts its performance - common approaches include:
            - Selecting the first or last element (simple but vulnerable to already-sorted arrays)
            - Choosing a random element (better average-case performance)
            - Using the "median-of-three" method (good balance of efficiency and reliability)

            Searching algorithms illustrate how different approaches can dramatically affect performance. Linear Search, while simple and applicable to unsorted data, becomes impractical for large datasets with its O(n) time complexity. Binary Search, requiring sorted data, achieves O(log n) by repeatedly dividing the search space in half. This dramatic improvement shows how additional constraints (sorted data) can enable more efficient algorithms.

            In graph algorithms, Breadth-First Search (BFS) and Depth-First Search (DFS) represent two fundamental approaches to traversing or searching graph structures. BFS explores all vertices at the current depth before moving to vertices at the next depth level, making it ideal for:
            - Finding shortest paths in unweighted graphs
            - Testing graph bipartiteness
            - Finding all nodes within one connected component

            DFS, on the other hand, explores as far as possible along each branch before backtracking, making it particularly useful for:
            - Topological sorting
            - Finding strongly connected components
            - Solving maze-like puzzles

            Dynamic Programming (DP) represents a powerful paradigm for solving complex problems by breaking them down into simpler subproblems. Unlike simple recursion, DP stores the results of subproblems to avoid redundant computation. The Fibonacci sequence calculation illustrates this perfectly:
            - Naive recursion recomputes the same values multiple times, leading to O(2ⁿ) complexity
            - DP with memoization stores computed values, reducing complexity to O(n)
            - Bottom-up DP eliminates recursion overhead and further improves space efficiency

            Greedy Algorithms make locally optimal choices at each step, hoping to find a global optimum. While this approach doesn't always yield the best solution, it often provides good approximations with better time complexity. Dijkstra's shortest path algorithm exemplifies this approach - at each step, it selects the unvisited vertex with the smallest tentative distance, eventually finding the shortest path to all vertices from the starting point.
        """,
        "programming_languages": """
                Programming languages serve as the interface between human logic and machine execution. Understanding their evolution, paradigms, and characteristics is crucial for effective software development.

                Python stands out as a high-level, interpreted language known for its readability and versatility. Its philosophy emphasizes code readability with notable use of whitespace indentation to delimit code blocks. Python's dynamic typing means variables can hold different types of values, and type checking happens at runtime. This flexibility comes with both advantages and considerations:

                Python's core features include:
                - Comprehensive standard library ("batteries included" philosophy)
                - Dynamic typing and automatic memory management
                - First-class functions enabling functional programming
                - Rich ecosystem of third-party packages via PyPI
                - Support for multiple programming paradigms

                Consider this Python example of list comprehension:
                numbers = [1, 2, 3, 4, 5]
                squares = [x**2 for x in numbers if x % 2 == 0]
                This concise syntax demonstrates Python's expressive power, accomplishing in one line what might take several lines in other languages.

                JavaScript, originally designed for client-side web programming, has evolved into a versatile language used across the full stack. Its event-driven, non-blocking architecture makes it particularly suitable for network applications. Key JavaScript concepts include:

                Asynchronous Programming:
                JavaScript handles asynchronous operations through:
                - Callbacks (traditional approach)
                - Promises (improved control flow)
                - Async/await (modern, more readable syntax)

                Example of asynchronous evolution:
                // Callbacks
                getData(function(result) {
                    processData(result, function(processed) {
                        saveData(processed);
                    });
                });

                // Modern async/await
                async function handleData() {
                    const result = await getData();
                    const processed = await processData(result);
                    await saveData(processed);
                }

                Java represents the object-oriented paradigm with its "write once, run anywhere" philosophy. It achieves platform independence through the Java Virtual Machine (JVM). Java's strong typing and compile-time checking help catch errors early in development.

                Java's key features include:
                - Strong type system
                - Extensive class libraries
                - Garbage collection
                - Multi-threading support
                - Platform independence

                Java's approach to object-oriented programming:
                public class BankAccount {
                    private double balance;
                    public synchronized void deposit(double amount) {
                        if (amount > 0) {
                            balance += amount;
                        }
                    }
                }
                This example demonstrates encapsulation, data validation, and thread safety.

                Each language has its own memory management approach:
                - Python uses reference counting with garbage collection
                - JavaScript employs mark-and-sweep garbage collection
                - Java uses generational garbage collection
                These differences impact performance characteristics and usage patterns.
            """,

            "databases": """
                Database systems form the backbone of modern data-driven applications, providing structured ways to store, retrieve, and manage data. Understanding database concepts involves both theoretical foundations and practical implementations.

                Relational Database Management Systems (RDBMS) organize data into tables (relations) with rows (tuples) and columns (attributes). The relational model, based on set theory and predicate logic, provides a mathematical foundation for database operations.

                Database Normalization is a systematic approach to reducing data redundancy and ensuring data integrity. The normal forms represent increasingly strict rules:

                First Normal Form (1NF):
                - Atomic values in each column
                - No repeating groups
                Example transformation:
                Before: Customer(ID, Name, Phone1, Phone2)
                After: Customer(ID, Name) and CustomerPhone(CustomerID, Phone)

                Second Normal Form (2NF):
                - Must be in 1NF
                - No partial dependencies on primary key
                This addresses situations where some columns depend only on part of the primary key.

                Third Normal Form (3NF):
                - Must be in 2NF
                - No transitive dependencies
                Example: If ZIP determines City, and City determines State, storing all three creates potential inconsistencies.

                SQL (Structured Query Language) provides a standardized way to interact with relational databases. Complex queries often involve:

                Joins: Combining data from multiple tables
                SELECT orders.id, customers.name, products.description
                FROM orders
                JOIN customers ON orders.customer_id = customers.id
                JOIN products ON orders.product_id = products.id
                WHERE orders.date >= '2023-01-01';

                Transaction Management ensures data consistency through ACID properties:
                - Atomicity: All operations complete successfully or none do
                - Consistency: Database remains in a valid state
                - Isolation: Concurrent transactions don't interfere
                - Durability: Committed changes persist

                Example transaction:
                BEGIN TRANSACTION;
                    UPDATE accounts SET balance = balance - 100 WHERE id = 1;
                    UPDATE accounts SET balance = balance + 100 WHERE id = 2;
                    -- Only if both updates succeed:
                    COMMIT;
                -- If any operation fails:
                ROLLBACK;

                NoSQL databases emerged to handle scenarios where relational databases prove limiting:

                Document Stores (e.g., MongoDB):
                {
                    "user_id": "12345",
                    "name": "John Doe",
                    "orders": [
                        {"id": "A1", "items": ["book", "pen"]},
                        {"id": "A2", "items": ["notebook"]}
                    ]
                }
                This flexible schema allows for nested data structures and easier scalability.

                Key-Value Stores (e.g., Redis):
                Perfect for caching and session management:
                SET session:user123 "{lastAccess: '2023-10-01', preferences: {...}}"
                GET session:user123

                Graph Databases (e.g., Neo4j):
                Ideal for relationship-heavy data:
                CREATE (john:Person {name: 'John'})-[:FOLLOWS]->(mary:Person {name: 'Mary'})

                Database Indexing significantly impacts performance:
                - B-tree indexes for range queries
                - Hash indexes for exact matches
                - Bitmap indexes for low-cardinality columns
                Understanding index types helps in query optimization.

                Query Optimization involves:
                - Analyzing execution plans
                - Proper index usage
                - Query rewriting
                - Statistics maintenance
                Example:
                EXPLAIN ANALYZE
                SELECT * FROM orders
                WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
                AND status = 'completed';
            """,
            "software_engineering": """
                    Software Engineering encompasses the systematic approach to developing, operating, and maintaining software systems. It combines technical expertise with project management and process methodologies to create reliable, scalable, and maintainable software solutions.

                    The Software Development Life Cycle (SDLC) provides a structured approach to software development:

                    Requirements Analysis and Planning:
                    This crucial first phase involves gathering and analyzing stakeholder needs. Requirements can be:
                    - Functional: Describing system behavior
                    - Non-functional: Performance, security, scalability
                    - Business: Cost constraints, market timing

                    Requirements gathering techniques include:
                    - User interviews and surveys
                    - Observation of existing systems
                    - Prototyping and user feedback
                    - Document analysis
                    - Workshop sessions with stakeholders

                    System Design comprises:

                    Architecture Design:
                    - Selecting appropriate architectural patterns
                    - Microservices vs Monolithic architecture
                    - Defining system boundaries and interfaces
                    - Planning for scalability and performance

                    Detailed Design:
                    - Component specifications
                    - Database schema design
                    - API definitions
                    - User interface mockups
                    - Security measures

                    Implementation Phase practices:
                    - Version Control Systems (Git workflows)
                    - Code Review processes
                    - Continuous Integration/Deployment (CI/CD)
                    - Test-Driven Development (TDD)
                    Example CI/CD pipeline:
                    1. Code commit triggers automated build
                    2. Unit tests and integration tests run
                    3. Code quality checks performed
                    4. Staging deployment for testing
                    5. Production deployment if all checks pass

                    Testing Strategies:
                    Unit Testing:
                    def test_user_registration():
                        user = create_user("john@example.com", "password123")
                        assert user.email == "john@example.com"
                        assert user.is_active == True

                    Integration Testing:
                    - Testing component interactions
                    - API endpoint testing
                    - Database integration testing

                    System Testing:
                    - End-to-end scenarios
                    - Performance testing
                    - Security testing
                    - User acceptance testing

                    Maintenance and Evolution:
                    - Bug fixing and patch management
                    - Feature enhancements
                    - Performance optimization
                    - Technical debt management
                    - Documentation updates

                    Agile Methodology emphasizes:
                    - Iterative development
                    - Regular customer feedback
                    - Cross-functional teams
                    - Adaptability to change

                    Scrum Framework implementation:
                    - Sprint Planning
                    - Daily Stand-ups
                    - Sprint Review
                    - Sprint Retrospective
                    - Product Backlog management

                    DevOps Practices integrate:
                    - Automated deployment
                    - Infrastructure as Code
                    - Monitoring and logging
                    - Incident response
                    - Configuration management

                    Example Infrastructure as Code (Terraform):
                    resource "aws_instance" "web_server" {
                      ami           = "ami-0c55b159cbfafe1f0"
                      instance_type = "t2.micro"
                      tags = {
                        Name = "WebServer"
                        Environment = "Production"
                      }
                    }
                """,

                "natural_language_processing": """
                    Natural Language Processing (NLP) bridges the gap between human communication and machine understanding. It combines linguistics, computer science, and artificial intelligence to enable computers to process and understand natural language.

                    Text Preprocessing Pipeline:
                    1. Tokenization breaks text into individual tokens:
                    "Hello, world!" → ["Hello", ",", "world", "!"]

                    Different tokenization approaches:
                    - Word tokenization
                    - Subword tokenization (BPE, WordPiece)
                    - Character tokenization

                    2. Normalization includes:
                    - Case folding: Converting to lowercase
                    - Accent removal
                    - Unicode normalization
                    Example:
                    "Café" → "cafe"

                    3. Stop Word Removal:
                    - Removing common words (the, is, at, which)
                    - Domain-specific stop words
                    - Impact on semantic meaning

                    Text Representation Models:

                    Bag of Words (BoW):
                    Text: "John likes to watch movies. Mary likes movies too."
                    BoW: {
                        "John": 1,
                        "likes": 2,
                        "to": 1,
                        "watch": 1,
                        "movies": 2,
                        "Mary": 1,
                        "too": 1
                    }

                    TF-IDF (Term Frequency-Inverse Document Frequency):
                    - Measures word importance in document collections
                    - tf(t,d) = count of term t in document d
                    - idf(t) = log(N/df(t)) where N is total documents
                    - tf-idf(t,d) = tf(t,d) * idf(t)

                    Word Embeddings revolutionized NLP:
                    Word2Vec models:
                    - Skip-gram: Predicts context words from target
                    - CBOW: Predicts target word from context
                    - Captures semantic relationships:
                      king - man + woman ≈ queen

                    Modern Transformer Architecture:
                    - Self-attention mechanisms
                    - Positional encoding
                    - Multi-head attention
                    Example attention calculation:
                    Attention(Q,K,V) = softmax(QK^T/√d_k)V

                    BERT (Bidirectional Encoder Representations):
                    - Pre-training tasks:
                      * Masked Language Modeling
                      * Next Sentence Prediction
                    - Fine-tuning for specific tasks:
                      * Classification
                      * Named Entity Recognition
                      * Question Answering

                    Practical NLP Applications:

                    Sentiment Analysis:
                    def analyze_sentiment(text):
                        tokens = preprocess(text)
                        features = extract_features(tokens)
                        return classifier.predict(features)

                    Named Entity Recognition (NER):
                    Text: "Microsoft Corporation is located in Redmond, Washington."
                    Entities: {
                        "Microsoft Corporation": ORGANIZATION,
                        "Redmond": LOCATION,
                        "Washington": LOCATION
                    }

                    Machine Translation:
                    - Sequence-to-sequence models
                    - Attention mechanisms
                    - Beam search decoding
                    Example architecture:
                    source_text → encoder → attention → decoder → target_text

                    Language Generation:
                    - Temperature sampling
                    - Top-k and Top-p sampling
                    - Beam search
                    Example:
                    def generate_text(prompt, max_length=100):
                        tokens = tokenize(prompt)
                        while len(tokens) < max_length:
                            next_token = model.predict_next(tokens)
                            tokens.append(next_token)
                        return detokenize(tokens)

                    Evaluation Metrics:
                    - BLEU score for translation
                    - ROUGE for summarization
                    - Perplexity for language models
                    - F1 score for NER
                """,
                "machine_learning": """
                        Machine Learning represents the core of artificial intelligence, enabling systems to learn from experience without explicit programming. The field encompasses various approaches to automated learning and pattern recognition.

                        Supervised Learning fundamentals:
                        The learning process involves training on labeled data pairs (X, y) where:
                        - X represents features/inputs
                        - y represents target/output

                        Linear Regression demonstrates basic supervised learning:
                        y = wx + b
                        where:
                        - w represents weights (parameters)
                        - b represents bias
                        - Cost function: Mean Squared Error (MSE)
                        MSE = (1/n)Σ(y_pred - y_actual)²

                        Gradient Descent Optimization:
                        - Updates parameters iteratively
                        - Learning rate controls step size
                        - Batch vs Mini-batch vs Stochastic
                        Example implementation:
                        def gradient_descent(X, y, w, b, learning_rate):
                            m = len(X)
                            for i in range(iterations):
                                predictions = w*X + b
                                error = predictions - y
                                w -= (learning_rate/m) * sum(error * X)
                                b -= (learning_rate/m) * sum(error)

                        Classification Algorithms:
                        Logistic Regression:
                        - Sigmoid function: σ(z) = 1/(1 + e^(-z))
                        - Binary classification boundary at 0.5
                        - Cross-entropy loss function

                        Support Vector Machines (SVM):
                        - Maximum margin hyperplane
                        - Kernel trick for non-linear separation
                        - Support vectors determine boundary

                        Decision Trees:
                        - Binary splitting based on features
                        - Information gain or Gini impurity
                        - Prone to overfitting if too deep
                        Example splitting criterion:
                        Information Gain = H(parent) - Σ(wi * H(childi))
                        where H is entropy and wi is proportion of samples

                        Neural Networks Architecture:

                        Feed-forward Neural Networks:
                        - Input layer: Raw features
                        - Hidden layers: Learned representations
                        - Output layer: Predictions
                        - Activation functions: ReLU, sigmoid, tanh

                        Convolutional Neural Networks (CNN):
                        - Convolutional layers for feature extraction
                        - Pooling layers for dimensionality reduction
                        - Fully connected layers for classification
                        Example architecture:
                        class CNN(nn.Module):
                            def __init__(self):
                                self.conv1 = nn.Conv2d(3, 64, kernel_size=3)
                                self.pool = nn.MaxPool2d(2, 2)
                                self.fc1 = nn.Linear(64 * 14 * 14, 10)

                        Unsupervised Learning approaches:

                        K-means Clustering:
                        1. Initialize k centroids randomly
                        2. Assign points to nearest centroid
                        3. Update centroids to cluster means
                        4. Repeat until convergence

                        Principal Component Analysis (PCA):
                        - Dimensionality reduction
                        - Preserves maximum variance
                        - Eigenvalue decomposition
                        Steps:
                        1. Standardize features
                        2. Compute covariance matrix
                        3. Calculate eigenvectors
                        4. Select top k components

                        Model Evaluation and Validation:

                        Cross-validation:
                        - K-fold splitting
                        - Stratified sampling
                        - Leave-one-out

                        Metrics:
                        - Accuracy: (TP + TN)/(TP + TN + FP + FN)
                        - Precision: TP/(TP + FP)
                        - Recall: TP/(TP + FN)
                        - F1 Score: 2*(Precision*Recall)/(Precision+Recall)

                        ROC and AUC:
                        - True Positive Rate vs False Positive Rate
                        - Area Under Curve measures discrimination

                        Regularization Techniques:
                        - L1 (Lasso): Sparse feature selection
                        - L2 (Ridge): Weight decay
                        - Dropout: Random neuron deactivation
                        - Early stopping: Prevent overfitting
                    """,

                    "web_development": """
                        Web Development encompasses the creation and maintenance of websites and web applications, combining frontend user interfaces with backend services and databases.

                        Frontend Development fundamentals:

                        HTML5 (Hypertext Markup Language):
                        - Semantic elements for better structure
                        - Accessibility considerations
                        - Forms and validation
                        Example semantic structure:
                        <header>
                            <nav>
                                <ul>
                                    <li><a href="#home">Home</a></li>
                                </ul>
                            </nav>
                        </header>
                        <main>
                            <article>
                                <section>
                                    <h1>Main Content</h1>
                                </section>
                            </article>
                        </main>

                        CSS3 (Cascading Style Sheets):
                        - Box model and layout
                        - Flexbox and Grid systems
                        - Responsive design
                        - Animations and transitions
                        Example responsive design:
                        @media screen and (max-width: 768px) {
                            .container {
                                flex-direction: column;
                                padding: 1rem;
                            }
                            .sidebar {
                                display: none;
                            }
                        }

                        JavaScript and Modern Features:
                        - ES6+ features
                        - Promises and async/await
                        - Modules and bundling
                        - DOM manipulation
                        Example modern JavaScript:
                        const fetchData = async () => {
                            try {
                                const response = await fetch('/api/data');
                                const data = await response.json();
                                return data;
                            } catch (error) {
                                console.error('Error:', error);
                            }
                        };

                        Frontend Frameworks:

                        React.js:
                        - Component-based architecture
                        - Virtual DOM
                        - State management (Redux, Context)
                        Example React component:
                        function UserProfile({ user }) {
                            const [isEditing, setIsEditing] = useState(false);
                            return (
                                <div className="profile">
                                    <h2>{user.name}</h2>
                                    {isEditing ? (
                                        <EditForm user={user} />
                                    ) : (
                                        <DisplayInfo user={user} />
                                    )}
                                </div>
                            );
                        }

                        Backend Development:

                        Node.js and Express:
                        - Event-driven architecture
                        - Middleware pattern
                        - RESTful API design
                        Example Express server:
                        const express = require('express');
                        const app = express();

                        app.use(express.json());

                        app.get('/api/users', async (req, res) => {
                            try {
                                const users = await User.find();
                                res.json(users);
                            } catch (error) {
                                res.status(500).send(error);
                            }
                        });

                        Database Integration:
                        - SQL vs NoSQL
                        - ORM (Object-Relational Mapping)
                        - Connection pooling
                        Example Mongoose schema:
                        const userSchema = new Schema({
                            username: { type: String, required: true },
                            email: { type: String, unique: true },
                            createdAt: { type: Date, default: Date.now }
                        });

                        Authentication and Security:
                        - JWT (JSON Web Tokens)
                        - OAuth integration
                        - CSRF protection
                        - XSS prevention
                        Example JWT implementation:
                        const generateToken = (user) => {
                            return jwt.sign(
                                { id: user.id },
                                process.env.JWT_SECRET,
                                { expiresIn: '24h' }
                            );
                        };

                        Web Security Best Practices:
                        - HTTPS implementation
                        - Content Security Policy
                        - Secure cookie handling
                        - Input validation
                        Example security middleware:
                        app.use(helmet());
                        app.use(cors());
                        app.use(rateLimit({
                            windowMs: 15 * 60 * 1000,
                            max: 100
                        }));

                        Performance Optimization:
                        - Code splitting
                        - Lazy loading
                        - Caching strategies
                        - Image optimization
                        Example React code splitting:
                        const UserDashboard = React.lazy(() =>
                            import('./components/UserDashboard')
                        );

                        Testing Strategies:
                        - Unit testing (Jest)
                        - Integration testing
                        - End-to-end testing (Cypress)
                        Example Jest test:
                        describe('User API', () => {
                            test('should create new user', async () => {
                                const response = await request(app)
                                    .post('/api/users')
                                    .send(userData);
                                expect(response.status).toBe(201);
                                expect(response.body).toHaveProperty('id');
                            });
                        });
                    """,
                    "operating_systems": """
                            Operating Systems (OS) serve as the fundamental software layer between hardware and applications, managing computer resources and providing essential services for both users and programs.

                            Process Management fundamentals:

                            Process States and Transitions:
                            - New: Process is being created
                            - Ready: Waiting to be assigned to processor
                            - Running: Instructions are being executed
                            - Waiting: Process waiting for I/O or event
                            - Terminated: Process has finished execution

                            Process Control Block (PCB) contains:
                            - Process ID and State
                            - Program Counter
                            - CPU registers
                            - CPU scheduling information
                            - Memory management information
                            - I/O status information

                            Context Switching mechanism:
                            1. Save current process state
                            2. Update PCB of current process
                            3. Move PCB to appropriate queue
                            4. Select new process
                            5. Update memory management structures
                            6. Restore new process state

                            CPU Scheduling Algorithms:

                            First-Come, First-Served (FCFS):
                            - Non-preemptive
                            - Simple implementation
                            - Can lead to convoy effect
                            Example sequence:
                            P1(burst=24) → P2(burst=3) → P3(burst=3)
                            Average waiting time = (0 + 24 + 27)/3 = 17

                            Shortest Job First (SJF):
                            - Can be preemptive or non-preemptive
                            - Optimal average waiting time
                            - Requires prediction of burst time
                            Example:
                            Process   Burst Time   Priority
                            P1          6            2
                            P2          8            1
                            P3          7            3
                            P4          3            4

                            Round Robin (RR):
                            - Time quantum based
                            - Preemptive
                            - Fair allocation
                            Implementation:
                            def round_robin(processes, quantum):
                                time = 0
                                while processes:
                                    current = processes.pop(0)
                                    if current.burst_time > quantum:
                                        time += quantum
                                        current.burst_time -= quantum
                                        processes.append(current)
                                    else:
                                        time += current.burst_time

                            Memory Management:

                            Paging System:
                            - Fixed-size blocks (pages)
                            - Page table for address translation
                            - Translation Lookaside Buffer (TLB)
                            Virtual address structure:
                            [Page Number | Offset]
                            Physical address translation:
                            Physical Address = (Page Table[Page Number] × Page Size) + Offset

                            Virtual Memory implementation:
                            - Demand paging
                            - Page replacement algorithms
                            - Thrashing prevention
                            Page replacement algorithms:
                            1. FIFO (First-In-First-Out)
                            2. LRU (Least Recently Used)
                            3. Clock algorithm

                            File Systems:

                            File System Structure:
                            - Boot block
                            - Superblock
                            - Inode blocks
                            - Data blocks

                            File Allocation Methods:
                            1. Contiguous Allocation:
                                - Fast sequential access
                                - External fragmentation

                            2. Linked Allocation:
                                - No external fragmentation
                                - Poor random access

                            3. Indexed Allocation:
                                - Efficient direct access
                                - Space overhead for index

                            Device Management:

                            Device Drivers:
                            - Character devices
                            - Block devices
                            - Network devices
                            Example driver structure:
                            struct device_driver {
                                int (*open)(struct device *);
                                ssize_t (*read)(struct device *, char *, size_t);
                                ssize_t (*write)(struct device *, const char *, size_t);
                                int (*close)(struct device *);
                            };

                            I/O Scheduling:
                            - SCAN (elevator) algorithm
                            - C-SCAN (circular SCAN)
                            - LOOK and C-LOOK variations
                        """,

                        "computer_networks": """
                            Computer Networks enable communication between computing devices, forming the backbone of modern digital connectivity through various protocols, architectures, and technologies.

                            OSI Model Layers:

                            Physical Layer (Layer 1):
                            - Bit transmission over physical medium
                            - Encoding and signaling
                            - Hardware specifications
                            Example specifications:
                            - Ethernet: 10BASE-T, 100BASE-TX
                            - Fiber optics: Single-mode, Multi-mode
                            - Wireless: 802.11 specifications

                            Data Link Layer (Layer 2):
                            - Framing
                            - Error detection and correction
                            - MAC addressing
                            Example frame structure:
                            [Preamble|Dest MAC|Source MAC|Type|Payload|FCS]

                            Network Layer (Layer 3):
                            - IP addressing and routing
                            - Packet forwarding
                            - Fragmentation and reassembly
                            Example IPv4 header:
                            - Version (4 bits)
                            - Header Length (4 bits)
                            - Total Length (16 bits)
                            - Time to Live (8 bits)
                            - Protocol (8 bits)
                            - Source IP (32 bits)
                            - Destination IP (32 bits)

                            Transport Layer (Layer 4):

                            TCP (Transmission Control Protocol):
                            - Connection-oriented
                            - Reliable delivery
                            - Flow control
                            - Congestion control
                            Three-way handshake:
                            1. SYN (Client → Server)
                            2. SYN-ACK (Server → Client)
                            3. ACK (Client → Server)

                            UDP (User Datagram Protocol):
                            - Connectionless
                            - No guarantee of delivery
                            - No flow control
                            - Lower overhead
                            Application scenarios:
                            - Real-time streaming
                            - DNS queries
                            - DHCP

                            Network Security:

                            Encryption Protocols:
                            - SSL/TLS
                            - IPSec
                            - WPA3
                            Example TLS handshake:
                            1. Client Hello (cipher suites)
                            2. Server Hello (selected cipher)
                            3. Certificate exchange
                            4. Key exchange
                            5. Finished

                            Firewall Implementation:
                            - Packet filtering
                            - Stateful inspection
                            - Application layer filtering
                            Example rule:
                            iptables -A INPUT -p tcp --dport 80 -j ACCEPT

                            Routing Protocols:

                            Interior Gateway Protocols:

                            RIP (Routing Information Protocol):
                            - Distance vector protocol
                            - Hop count metric
                            - Maximum 15 hops

                            OSPF (Open Shortest Path First):
                            - Link state protocol
                            - Dijkstra's algorithm
                            - Area-based hierarchy
                            Example OSPF process:
                            1. Hello packets for neighbor discovery
                            2. Database synchronization
                            3. Shortest path calculation
                            4. Routing table update

                            Exterior Gateway Protocols:

                            BGP (Border Gateway Protocol):
                            - Path vector protocol
                            - Policy-based routing
                            - AS path attribute
                            Example BGP attributes:
                            - AS_PATH
                            - NEXT_HOP
                            - LOCAL_PREF
                            - MED

                            Network Services:

                            DNS (Domain Name System):
                            - Hierarchical naming
                            - Distributed database
                            - Caching mechanisms
                            Example record types:
                            - A (IPv4 address)
                            - AAAA (IPv6 address)
                            - MX (mail server)
                            - CNAME (alias)

                            DHCP (Dynamic Host Configuration Protocol):
                            - Automatic IP configuration
                            - Address pool management
                            - Lease time control
                            DHCP process:
                            1. DISCOVER
                            2. OFFER
                            3. REQUEST
                            4. ACKNOWLEDGE

                            Quality of Service (QoS):
                            - Traffic classification
                            - Queue management
                            - Congestion avoidance
                            Example mechanisms:
                            - DiffServ
                            - IntServ
                            - RSVP
                        """,


    # Add more topics as needed
}

# Training data structure for generating questions
TRAINING_DATA = {
    "python": [
            {
                "context": "Python uses dynamic typing which allows variable type changes. Basic types include int, float, str, bool, and complex types include list, tuple, dict, set.",
                "question": "What is dynamic typing in Python and how does it work?",
                "correct_answer": "Dynamic typing allows variables to change types during runtime, meaning a variable can hold different types of values at different times without explicit type declaration.",
                "wrong_answers": [
                    "Dynamic typing means variables must be declared with their type before use.",
                    "Dynamic typing only allows variables to hold numerical values.",
                    "Dynamic typing requires explicit type conversion for every variable assignment."
                ]
            },
            {
                "context": "List comprehensions provide a concise way to create lists. Traditional loop: squares = [] for x in range(10): squares.append(x**2) List comprehension: squares = [x**2 for x in range(10)]",
                "question": "How do list comprehensions improve Python code compared to traditional loops?",
                "correct_answer": "List comprehensions provide a more concise and readable way to create lists in a single line, combining the loop and list creation into one expression.",
                "wrong_answers": [
                    "List comprehensions always execute faster than traditional loops regardless of complexity.",
                    "List comprehensions can only be used for simple mathematical operations.",
                    "List comprehensions eliminate the need for iteration in Python code."
                ]
            },
            {
                "context": "Decorators are a way to modify function behavior. def timer(func): def wrapper(*args, **kwargs): start = time.time() result = func(*args, **kwargs) end = time.time() print(f'{func.__name__} took {end-start} seconds') return result return wrapper",
                "question": "What is the primary purpose of decorators in Python?",
                "correct_answer": "Decorators modify or enhance function behavior without directly changing the function's code, allowing for code reuse and separation of concerns.",
                "wrong_answers": [
                    "Decorators are only used for timing function execution in Python.",
                    "Decorators directly modify the source code of the functions they decorate.",
                    "Decorators are used exclusively for handling exceptions in functions."
                ]
            },
            {
                "context": "Exception handling in Python uses try-except blocks: try: result = risky_operation() except ValueError as e: print(f'Value error: {e}') except (TypeError, KeyError) as e: print(f'Type or Key error: {e}') else: print('Operation succeeded') finally: cleanup_resources()",
                "question": "How does Python's exception handling mechanism work with try-except blocks?",
                "correct_answer": "Python's try-except blocks catch and handle exceptions during execution, with optional else and finally clauses for successful execution and cleanup respectively.",
                "wrong_answers": [
                    "Try-except blocks prevent all errors from occurring in Python code.",
                    "Exception handling only works with built-in Python exceptions, not custom ones.",
                    "The finally clause only executes when an exception occurs."
                ]
            },
            {
                "context": "Generators in Python use yield to produce a sequence of values over time: def fibonacci(n): a, b = 0, 1 for _ in range(n): yield a a, b = b, a + b",
                "question": "What are generators in Python and how do they differ from regular functions?",
                "correct_answer": "Generators are functions that use yield to return values one at a time, maintaining their state between calls and consuming less memory than returning a complete list.",
                "wrong_answers": [
                    "Generators always return all values at once like regular functions.",
                    "Generators can only be used with numerical sequences.",
                    "Generators must be converted to lists before their values can be accessed."
                ]
            }
        ],
    "data_structures": [
        {
            "context": "Arrays are fixed-size collections of elements with same data type, providing O(1) access time for elements using their index positions. However, arrays come with limitations - their size is typically fixed at creation time, and inserting or deleting elements can be expensive as it might require shifting many elements.",
            "question": "What are the key characteristics and limitations of arrays in data structures?",
            "correct_answer": "Arrays are fixed-size collections with O(1) access time, but have limitations including fixed size and expensive insertion/deletion operations requiring element shifting.",
            "wrong_answers": [
                "Arrays are dynamic collections that can grow and shrink automatically with O(n) access time.",
                "Arrays provide efficient insertion and deletion but have slow access time for individual elements.",
                "Arrays are linked structures where each element points to the next element in memory."
            ]
        },
        {
            "context": "Hash Tables combine array-like access speed with dynamic size management through a hash function that converts keys into array indices. A good hash function distributes elements uniformly across the available space, enabling O(1) average case performance for insertions, deletions, and lookups.",
            "question": "How do Hash Tables achieve efficient data access and storage?",
            "correct_answer": "Hash Tables use a hash function to convert keys into array indices, providing O(1) average case performance for operations through uniform distribution of elements.",
            "wrong_answers": [
                "Hash Tables store elements in sorted order using binary search trees for efficient access.",
                "Hash Tables maintain a linked list of all elements for quick insertion and deletion operations.",
                "Hash Tables use sequential storage with linear search for finding elements."
            ]
        }
    ],
    "algorithms": [
        {
            "context": "Quick Sort selects a 'pivot' element and partitions the array around it, placing smaller elements before and larger elements after. While its worst-case time complexity is O(n²), its average case performance of O(n log n) and in-place operation make it highly efficient in practice.",
            "question": "What makes Quick Sort an efficient sorting algorithm despite its worst-case complexity?",
            "correct_answer": "Quick Sort's average case performance of O(n log n) and in-place operation make it efficient, using a pivot-based partitioning strategy.",
            "wrong_answers": [
                "Quick Sort always guarantees O(n log n) performance regardless of input data.",
                "Quick Sort uses additional memory proportional to input size for sorting.",
                "Quick Sort performs better than all other sorting algorithms in worst-case scenarios."
            ]
        }
    ],
    "algorithms": [
            {
                "context": "Merge Sort employs a divide-and-conquer strategy. It splits the array into smaller subarrays, sorts them independently, and then merges these sorted subarrays. This approach guarantees O(n log n) time complexity regardless of the input data's initial order.",
                "question": "Why is Merge Sort considered a stable sorting algorithm with guaranteed performance?",
                "correct_answer": "Merge Sort guarantees O(n log n) time complexity in all cases by using divide-and-conquer and maintaining relative order of equal elements during merging.",
                "wrong_answers": [
                    "Merge Sort performs sorting in-place without requiring additional memory space.",
                    "Merge Sort achieves O(n) time complexity by avoiding multiple comparisons.",
                    "Merge Sort uses pivot elements to partition data like Quick Sort."
                ]
            },
            {
                "context": "Dynamic Programming solves complex problems by breaking them down into simpler subproblems. Unlike simple recursion, DP stores the results of subproblems to avoid redundant computation. The Fibonacci sequence calculation illustrates this perfectly.",
                "question": "How does Dynamic Programming improve upon recursive solutions?",
                "correct_answer": "Dynamic Programming stores previously calculated results to avoid redundant computations, significantly improving efficiency by trading memory for speed.",
                "wrong_answers": [
                    "Dynamic Programming always uses less memory than recursive solutions.",
                    "Dynamic Programming only works with numerical sequences.",
                    "Dynamic Programming eliminates the need for recursive calls entirely."
                ]
            }
        ],

        "data_structures": [
            {
                "context": "Binary Search Trees (BST) maintain elements in sorted order with each node having at most two children. All left descendants have smaller values and all right descendants have larger values than the node itself.",
                "question": "What makes Binary Search Trees efficient for searching operations?",
                "correct_answer": "BSTs allow elimination of half the remaining elements at each step during search by comparing with the current node and choosing left or right subtree.",
                "wrong_answers": [
                    "BSTs store elements in arrays for constant-time access.",
                    "BSTs require searching both subtrees to find any element.",
                    "BSTs maintain elements in random order for better distribution."
                ]
            },
            {
                "context": "Graph traversal algorithms like Breadth-First Search (BFS) and Depth-First Search (DFS) serve different purposes. BFS explores all vertices at the current depth before moving to vertices at the next depth level.",
                "question": "When would you choose BFS over DFS for graph traversal?",
                "correct_answer": "BFS is preferred when finding shortest paths in unweighted graphs or when exploring closest neighbors first, as it visits nodes level by level.",
                "wrong_answers": [
                    "BFS uses less memory than DFS in all cases.",
                    "BFS is always faster than DFS regardless of graph structure.",
                    "BFS is only useful for trees, not general graphs."
                ]
            }
        ],

        "web_development": [
            {
                "context": "React.js uses a Virtual DOM and component-based architecture. When state changes occur, React first updates the Virtual DOM, compares it with the actual DOM, and then efficiently updates only the necessary parts of the real DOM.",
                "question": "How does React's Virtual DOM improve application performance?",
                "correct_answer": "The Virtual DOM allows React to batch and optimize DOM updates by comparing virtual and actual DOMs, minimizing expensive direct DOM manipulations.",
                "wrong_answers": [
                    "The Virtual DOM eliminates the need for any DOM manipulation.",
                    "The Virtual DOM makes all React applications faster than vanilla JavaScript.",
                    "The Virtual DOM stores all application data permanently."
                ]
            },
            {
                "context": "JWT (JSON Web Tokens) provide a stateless authentication mechanism. Each token contains encoded user information and is signed to ensure integrity, allowing servers to verify the token's authenticity without storing session data.",
                "question": "What are the main advantages of using JWT for authentication?",
                "correct_answer": "JWTs enable stateless authentication by containing encoded user data and signatures, reducing server storage needs while ensuring data integrity.",
                "wrong_answers": [
                    "JWTs provide complete protection against all types of security attacks.",
                    "JWTs eliminate the need for database user storage.",
                    "JWTs can only be used with REST APIs."
                ]
            }
        ],

        "operating_systems": [
            {
                "context": "Process scheduling algorithms like Round Robin assign each process a fixed time quantum. If a process doesn't complete within its quantum, it's moved to the back of the ready queue, ensuring fair CPU time distribution.",
                "question": "Why is Round Robin scheduling considered fair but not always optimal?",
                "correct_answer": "Round Robin ensures fair CPU distribution by giving each process equal time quanta, but may cause more context switches and be suboptimal for processes with varying CPU burst times.",
                "wrong_answers": [
                    "Round Robin always provides the best average waiting time.",
                    "Round Robin eliminates the need for context switching.",
                    "Round Robin only works with single-core processors."
                ]
            },
            {
                "context": "Virtual Memory uses demand paging to load only needed pages into physical memory. Page replacement algorithms like LRU (Least Recently Used) decide which pages to remove when memory is full.",
                "question": "How does demand paging with LRU improve memory management?",
                "correct_answer": "Demand paging with LRU optimizes memory usage by loading only required pages and replacing least recently used pages when needed, reducing memory waste.",
                "wrong_answers": [
                    "Demand paging eliminates the need for physical memory.",
                    "LRU guarantees no page faults will occur.",
                    "Virtual memory can only use LRU for page replacement."
                ]
            }
        ],

        "computer_networks": [
            {
                "context": "TCP's three-way handshake establishes a connection through SYN, SYN-ACK, and ACK packets. This process ensures both parties are ready to communicate and agree on initial sequence numbers.",
                "question": "Why is TCP's three-way handshake necessary for reliable communication?",
                "correct_answer": "The three-way handshake establishes synchronized sequence numbers and confirms both parties' readiness to communicate, enabling reliable, ordered data transmission.",
                "wrong_answers": [
                    "The three-way handshake is only needed for secure HTTPS connections.",
                    "TCP handshake prevents all types of network attacks.",
                    "Handshaking is optional in modern TCP implementations."
                ]
            },
            {
                "context": "DHCP automates IP address configuration through a four-step process: DISCOVER, OFFER, REQUEST, and ACKNOWLEDGE. This eliminates the need for manual IP configuration on each network device.",
                "question": "What makes DHCP essential in modern networks?",
                "correct_answer": "DHCP automates IP address management and network configuration, reducing administrative overhead and preventing address conflicts in large networks.",
                "wrong_answers": [
                    "DHCP is only needed for wireless networks.",
                    "DHCP provides network security features.",
                    "DHCP speeds up network communication."
                ]
            }
        ]

}
