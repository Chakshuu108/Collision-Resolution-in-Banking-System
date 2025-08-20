<h1>Banking System with Hash Table (C++)</h1>

<h2>Overview:</h2>
<ul>
<li>A console-based banking system developed in C++.</li>
<li>Efficiently manages multiple accounts using a hash table with cubic probing.</li>
<li>Supports standard banking operations like creating, depositing, withdrawing, searching, and deleting accounts.</li>
<li>Demonstrates use of <b>OOP concepts, dynamic memory allocation, and custom data structures</b>.</li>
</ul>

<h2>Key Features:</h2>
<h3>1. Account Management:</h3>
<ul>
<li>Each account has a unique 7-digit account number.</li>
<li>Stores account holder's name, balance, email, and phone number.</li>
<li>Ensures minimum deposit and withdrawal of 1000.</li>
</ul>

<h3>2. Admin-Only Operations:</h3>
<ul>
<li>Display all accounts in the system.</li>
<li>Check the current load factor of the hash table.</li>
<li>Protected using a secure admin password.</li>
</ul>

<h3>3. Hash Table Implementation:</h3>
<ul>
<li>Uses cubic probing for collision resolution.</li>
<li>Supports rehashing when load factor reaches 0.7 for optimal performance.</li>
<li>Ensures fast insertion, search, and deletion with amortized O(1) complexity.</li>
</ul>

<h3>4. Security & Validation:</h3>
<ul>
<li>Validates that account numbers are exactly 7 digits.</li>
<li>Deposits and withdrawals are validated to meet the minimum threshold.</li>
<li>Admin operations require password authentication.</li>
</ul>

<h2>Classes:</h2>
<h3>Account:</h3>
<ul>
<li>Stores individual account details.</li>
<li>Methods: deposit(), withdraw(), displayAccount(), and getters.</li>
</ul>

<h3>HashTable:</h3>
<ul>
<li>Manages accounts using hashing with cubic probing.</li>
<li>Handles collisions and deleted accounts effectively.</li>
<li>Methods: insertAccount(), searchAccount(), deleteAccount(), displayAll(), getLoadFactor(), rehash().</li>
</ul>

<h2>Workflow:</h2>
<ol>
<li>User chooses an operation from the menu (create, deposit, withdraw, search, delete).</li>
<li>System computes the hash index using the account number.</li>
<li>If collisions occur, cubic probing is applied to find the next available slot.</li>
<li>Accounts are dynamically stored in the hash table, ensuring fast access.</li>
<li>Admin-only operations require password authentication for security.</li>
<li>Load factor is monitored, and rehashing occurs automatically when necessary.</li>
</ol>

<h2>Benefits:</h2>
<ul>
<li>Efficient memory usage with dynamic allocation.</li>
<li>Fast operations even with large numbers of accounts.</li>
<li>Secure and robust design suitable for real-world banking simulations.</li>
</ul>


