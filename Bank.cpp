#include<iostream>
#include<vector>
#include <string>
#include <stdexcept> // needed for invalid_argument
using namespace std;

class Account{
    long long acnt_no;
    string name;
    double balance;
    string email;
    string phone;

    public:
    Account(long long acnt_no,string name,double balance ,string email,string phone) {
        //i made the acnt number to be 7 digits 
        if (acnt_no >= 1000000 && acnt_no <= 9999999) {
            this->acnt_no=acnt_no;
        } else {
            throw invalid_argument("Account number must be 7 digits!");
        }
        this->name=name;
        this->balance=(balance>=0)?balance:0.0;
        this->email=email;
        this->phone = phone;
    }

    //// as it is private access so we need to make getters so that they can fetch the info :
    long long getAccountNumber() { return acnt_no; }
    string getName() { return name; }
    double getBalance() { return balance; }
    string getEmail() { return email; }
    string getPhone() { return phone; }

    void deposit(double amount){
        // add money to balance
        if(amount>=1000) {
            balance+=amount;
            cout << "Deposited: " << amount << " successfully.\n";
        } else {
            cout << "Deposit must be at least 1000.\n";
        }

    }     
    void withdraw(double amount){  
        // subtract money from balance 
        if(amount<=balance && amount>=1000) {
            balance-=amount;
        } else {
            cout<<"Invalid withdrawal. Must be more than 1000"<<endl;
        }
    }


     void displayAccount() {
        cout << "--- Account Details ---"<<endl;
        cout << "Account Number: " << acnt_no<<endl;
        cout << "Name: " << name << endl;
        cout << "Balance: " << balance << endl;
        cout << "Email: " << email << endl;
        cout << "Phone: " << phone << endl;
        cout << "-----------------------"<<endl;
    }  
};

class HashTable {
    private:
        vector<Account*> table;
        vector<int> status;   // 0=empty, 1=occupied, 2=deleted
        int capacity; //size of the table 
        int size;     // number of active accounts

    public:
    HashTable(int capacity){
        this->capacity = capacity;
        table.resize(capacity, nullptr); // initialize slots with nullptr
        status.resize(capacity, 0);      // all slots are initially empty 
        size =0;
    }
    
    //hashing functions :
    //key is the acnt number that user will enter 
    
    //1. Linear Hashing :
    int hash1(long long key) const {
        return key % capacity;
    }

    //2. Double Hashing : Not Necessary to apply this 
    int hash2(long long key) const {
        // Must be non-zero and less than capacity
        return 1 + (key % (capacity - 1));
    }

    //3. Cubic Hashing:
    //baseIndex is the slot where the account should go 
     int probe(int baseIndex, int i) const {
        return (baseIndex + i * i * i) % capacity;
    }


    // ---------user functions :

    //1.
    void insertAccount(Account* acc){

        if(getLoadFactor() >= 0.7) {
            cout << "Load factor >= 0.7, rehashing..." << endl;
            rehash();
        }
        //step 1 - fetch acnt number
        long long key = acc->getAccountNumber();
        //step 2 - get base idx using linear prob :
        int baseidx=hash1(key);
        //step 3 - handle collision:

        int i = 0 ;
        int idx = baseidx;
                 //checl if it is occupied
        while(status[idx]==1) {
            i++;
            idx=probe(baseidx,i);
            if(i >= capacity) {     // table full
            cout << "Hash table is full"<<endl;
            return;
        }
        }

        //step 4 - insertion to the idx :
        table[idx] = acc;
    status[idx] = 1;
    cout << "Inserted account " << key << " at index " << idx << endl;

    }


    //2.
    Account* searchAccount(long long key) {
        //step 1 - base index using lin prob :
        int baseidx = hash1(key);
        //step 2 - if slot is not empty then return the acnt number :

        int idx;
        for (int i = 0; i < capacity; i++) {
            idx = probe(baseidx, i);

            if (status[idx] == 0) {
                // 0- empty slot so return null 
                return nullptr;
            }
            //if slot mein jagah h and the key is same to the acnt number stored 
            if (status[idx] == 1 && table[idx]->getAccountNumber() == key) {
                // acnt found
                return table[idx];
            }
             
    }

        return nullptr; // not found after loop 
        
    }

//3.
    bool deleteAccount(long long key) {
    // Step 1: Compute base index using hash1(key)
    int baseidx = hash1(key);
    // Step 2: 
    int idx = 0;
    for(int i =  0 ; i<capacity;i++) {
        idx =probe(baseidx,i);
        
        if(status[idx]==0) {
            //acnt is already not their :
            return false;
        }

        if(status[idx]==1 && table[idx]->getAccountNumber() ==key) {
            //acnt found dlt it :
            status[idx]=2;
            table[idx]=nullptr;
            size--;
            cout << "Deleted account " << key << " from index " << idx << endl;
            return true;
        
        }
    }
        return false; //not found after loop 
    }

    //4.
    void displayAll() {
        for(int i = 0 ; i<capacity;i++) {
            if(status[i]==1 && table[i]!=NULL) {
                cout<<"Index "<<i<<":" <<endl;
                table[i]->displayAccount();
            }
        }
    }

    double getLoadFactor() const {
        //static_cast ensures u get a decimal value 
        return static_cast<double>(size) / capacity;
    }

    void rehash() {
        int oldCaps = capacity;
        //creating new  table  vector:
        vector<Account*> oldTable = table;
        vector<int> oldStatus = status;
        
        //double the caps :
        capacity*=2;

        //create new tabble:
        table.clear();
        status.clear();
        //initialize the table with new doubled caps 
        table.resize(capacity,nullptr);
        status.resize(capacity,0);
        size = 0;

        //insert the existing accounts :
        for(int i = 0 ; i<oldCaps;i++){
            if(oldStatus[i]==1 && oldTable[i]!=nullptr) {
                //reinserting handles all the collisions automatically 
                insertAccount(oldTable[i]);
            }
            cout << "Rehashing done! New capacity: " << capacity << endl;
        }
    }
};




int main() {
    int capacity;
    cout << "Enter initial hash table capacity: ";
    cin >> capacity;

    HashTable hashTable(capacity);
    int choice;

    do {
        cout << "\n----- Banking System Menu -----\n";
        cout << "1. Create New Account\n";
        cout << "2. Deposit Money\n";
        cout << "3. Withdraw Money\n";
        cout << "4. Search Account\n";
        cout << "5. Delete Account\n";
        cout << "6. Display All Accounts\n";
        cout << "7. Show Load Factor\n";
        cout << "8. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch(choice) {
            case 1: {
                long long acnt_no;
                string name ,email,phone;
                double balance;
                cout<<"Enter 7-digit Account Number : ";
                cin>>acnt_no;
                cin.ignore();//ignore leftover newline for skipping inputs
                cout<<"Enter Name : ";
                
                getline(cin,name);
                cout << "Enter Initial Balance: ";
                cin >> balance;
                cout << "Enter Email: ";
                cin >> email;
                cout << "Enter Phone Number: ";
                cin >> phone;

                //insert the account :
                Account* acc = new Account(acnt_no, name, balance, email, phone);
                hashTable.insertAccount(acc);
                break;
            }

            case 2:{
                long long acnt_no;
                double amount;
                cout << "Enter Account Number: ";
                cin >> acnt_no;
                Account* acc = hashTable.searchAccount(acnt_no);
                if(acc) {
                    cout << "Enter amount to deposit (>=1000): ";
                    cin >> amount;
                    acc->deposit(amount);
                } else {
                    cout << "Account not found"<<endl;
                }
                break;
            }

            case 3:{
                long long acnt_no;
                double amount;
                cout << "Enter Account Number: ";
                cin >> acnt_no;
                Account* acc = hashTable.searchAccount(acnt_no);
                if(acc) {
                    cout << "Enter amount to withdraw (>=1000): ";
                    cin >> amount;
                    acc->withdraw(amount);
                } else {
                    cout << "Account not found!\n";
                }
                break;

            }

            case 4:{
                long long acnt_no;
                cout << "Enter Account Number to search: ";
                cin >> acnt_no;
                Account* acc = hashTable.searchAccount(acnt_no);
                if(acc) {
                    acc->displayAccount();
                } else {
                    cout << "Account not found"<<endl;
                }
                break;
            }

            case 5:{
                long long acnt_no;
                cout << "Enter Account Number to delete: ";
                cin >> acnt_no;
                if(!hashTable.deleteAccount(acnt_no)) {
                    cout << "Account not found!\n";
                }
                break;

            }
            case 6: {
                string adminPassword;
                cout << "Enter admin password to display all accounts: ";
                cin >> adminPassword;

                if(adminPassword == "Chakshu108") { 
                    hashTable.displayAll();
                } else {
                    cout << "Access Denied! Incorrect password."<<endl;
                }
                break;
            }

            case 7: {
                string adminPassword;
                cout << "Enter admin password to view load factor: ";
                cin >> adminPassword;

                if(adminPassword == "Chakshu108") {
                    cout << "Current Load Factor: " << hashTable.getLoadFactor() << endl;
                } else {
                    cout << "Access Denied! Incorrect password."<<endl;
                }
                break;
            }
            
            case 8:{
                cout << "Exiting program. Goodbye!"<<endl<<"Visit Again!";
                break;

            }
            default:
                cout << "Invalid choice! Try again.\n";
        }      
    }while(choice!=8);
    
    
    return 0;
}



