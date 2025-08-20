<h2>Banking System with Hash Table (C++)</h2>

<b>Overview:</b><br>
- A console-based banking system developed in C++.<br>
- Efficiently manages multiple accounts using a hash table with cubic probing.<br>
- Supports all standard banking operations like creating, depositing, withdrawing, searching, and deleting accounts.<br>
- Demonstrates use of <b>OOP concepts, dynamic memory allocation, and custom data structures</b>.<br><br>

<b>Key Features:</b><br>
1. <b>Account Management:</b><br>
&nbsp;&nbsp;- Each account has a unique 7-digit account number.<br>
&nbsp;&nbsp;- Stores account holder's name, balance, email, and phone number.<br>
&nbsp;&nbsp;- Ensures minimum deposit and withdrawal of 1000.<br><br>

2. <b>Admin-Only Operations:</b><br>
&nbsp;&nbsp;- Display all accounts in the system.<br>
&nbsp;&nbsp;- Check the current load factor of the hash table.<br>
&nbsp;&nbsp;- Protected using a secure admin password.<br><br>

3. <b>Hash Table Implementation:</b><br>
&nbsp;&nbsp;- Uses cubic probing for collision resolution.<br>
&nbsp;&nbsp;- Supports rehashing when load factor reaches 0.7 for optimal performance.<br>
&nbsp;&nbsp;- Ensures fast insertion, search, and deletion with amortized O(1) complexity.<br><br>

4. <b>Security & Validation:</b><br>
&nbsp;&nbsp;- Validates that account numbers are exactly 7 digits.<br>
&nbsp;&nbsp;- Deposits and withdrawals are validated to meet the minimum threshold.<br>
&nbsp;&nbsp;- Admin operations require password authentication.<br><br>

<b>Classes:</b><br>
- <b>Account:</b><br>
&nbsp;&nbsp;- Stores individual account details.<br>
&nbsp;&nbsp;- Methods: deposit(), withdraw(), displayAccount(), and getters.<br><br>

- <b>HashTable:</b><br>
&nbsp;&nbsp;- Manages accounts using hashing with cubic probing.<br>
&nbsp;&nbsp;- Handles collisions and deleted accounts effectively.<br>
&nbsp;&nbsp;- Methods include: insertAccount(), searchAccount(), deleteAccount(), displayAll(), getLoadFactor(), rehash().<br><br>

<b>Workflow:</b><br>
1. User chooses an operation from the menu (create, deposit, withdraw, search, delete).<br>
2. System computes the hash index using the account number.<br>
3. If collisions occur, cubic probing is applied to find the next available slot.<br>
4. Accounts are dynamically stored in the hash table, ensuring fast access.<br>
5. Admin-only operations require password authentication for security.<br>
6. Load factor is monitored, and rehashing occurs automatically when necessary.<br><br>

<b>Benefits:</b><br>
- Efficient memory usage with dynamic allocation.<br>
- Fast operations even with large numbers of accounts.<br>
- Secure and robust design suitable for real-world banking simulations.<br><br>

<b>Future Improvements:</b><br>
- Persistent storage using file I/O for saving accounts.<br>
- Account-level login authentication.<br>
- GUI integration for better user experience.<br>
- Additional banking features like fund transfers and transaction history.<br>
