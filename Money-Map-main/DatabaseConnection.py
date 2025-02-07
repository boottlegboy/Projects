from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb+srv://jesusdiaz1403:b1mRAtZw3MK5Q5eO@moneymap.mpksh.mongodb.net/")

db = client["MoneyMap"]

userInfo = db["User"]


def userData():
    user_info = {}
    user_info["MonthlyIncome"] = float(input("Enter your monthly income: "))
    user_info["MonthlyExpenses"] = float(input("Enter your monthly expenses: "))
    user_info["Checking"] = float(input("Enter your checking account balance: "))
    user_info["Savings"] = float(input("Enter your savings account balance: "))
    user_info["CreditCard"] = float(input("Enter your credit card balance: "))
    user_info["Loans"] = float(input("Enter your loan balance: "))


def save_user(user_Data):
    userInfo.insert_one(user_Data)
    print("User Info Updated!")


def get_user(username):
    return userInfo.find_one({"username": username})


def verify_user(username, password):
    user = get_user(username)
    if user:
        stored_password = user.get("password").encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True
    return False


def save_checking_account(username, account_data):
    user = userInfo.find_one({"username": username})
    if user:
        if "checking_accounts" not in user:
            user["checking_accounts"] = []
        user["checking_accounts"].append(account_data)
        userInfo.update_one({"username": username}, {"$set": {"checking_accounts": user["checking_accounts"]}})
        print(f"Checking account '{account_data['account_name']}' saved for user {username}.")
    else:
        print(f"User {username} not found.")


def get_checking_accounts(username):
    user = userInfo.find_one({"username": username}, {"checking_accounts": 1, "_id": 0})
    if user and "checking_accounts" in user:
        return user["checking_accounts"]
    return []


def update_checking_account(username, account_name, updated_account_data):
    user = userInfo.find_one({"username": username})
    if user:
        accounts = user.get("checking_accounts", [])
        # Find the account to update
        for account in accounts:
            if account["account_name"] == account_name:
                # Update account details
                account.update(updated_account_data)
                break
        # Save updated accounts back to the database
        userInfo.update_one(
            {"username": username},
            {"$set": {"checking_accounts": accounts}}
        )
        print(f"Checking account '{account_name}' updated for user {username}.")
    else:
        print(f"User {username} not found.")


def account_exists(username, account_name):
    user = userInfo.find_one({"username": username}, {"checking_accounts": 1, "_id": 0})
    if user and "checking_accounts" in user:
        return any(account["account_name"] == account_name for account in user["checking_accounts"])
    return False


def delete_checking_account(username, account_name):
    user = userInfo.find_one({"username": username})
    if user:
        accounts = user.get("checking_accounts", [])
        # Filter out the account to delete
        updated_accounts = [acc for acc in accounts if acc["account_name"] != account_name]
        # Save updated accounts back to the database
        userInfo.update_one(
            {"username": username},
            {"$set": {"checking_accounts": updated_accounts}}
        )
        print(f"Checking account '{account_name}' deleted for user {username}.")
    else:
        print(f"User {username} not found.")


def get_savings_accounts(username):
    user = userInfo.find_one({"username": username}, {"savings_accounts": 1, "_id": 0})
    if user and "savings_accounts" in user:
        return user["savings_accounts"]
    return []


def save_savings_account(username, account_data):
    userInfo.update_one(
        {"username": username},
        {"$push": {"savings_accounts": account_data}}
    )


def update_savings_account(username, account_name, updated_account_data):
    user = userInfo.find_one({"username": username})
    if user:
        accounts = user.get("savings_accounts", [])
        for account in accounts:
            if account["account_name"] == account_name:
                account.update(updated_account_data)
                break
        userInfo.update_one(
            {"username": username},
            {"$set": {"savings_accounts": accounts}}
        )


def delete_savings_account(username, account_name):
    userInfo.update_one(
        {"username": username},
        {"$pull": {"savings_accounts": {"account_name": account_name}}}
    )


def get_expense_accounts(username):
    user = userInfo.find_one({"username": username}, {"expenses": 1, "_id": 0})
    if user and "expenses" in user:
        return user["expenses"]
    return []


def save_expense_account(username, expense_data):
    userInfo.update_one(
        {"username": username},
        {"$push": {"expenses": expense_data}}
    )


def update_expense_account(username, expense_name, updated_expense_data):
    user = userInfo.find_one({"username": username})
    if user:
        expenses = user.get("expenses", [])
        for expense in expenses:
            if expense["expense_name"] == expense_name:
                expense.update(updated_expense_data)
                break
        userInfo.update_one(
            {"username": username},
            {"$set": {"expenses": expenses}}
        )


def delete_expense_account(username, expense_name):
    userInfo.update_one(
        {"username": username},
        {"$pull": {"expenses": {"expense_name": expense_name}}}
    )


def get_income_accounts(username):
    user = userInfo.find_one({"username": username}, {"incomes": 1, "_id": 0})
    if user and "incomes" in user:
        return user["incomes"]
    return []


def save_income_account(username, income_data):
    userInfo.update_one(
        {"username": username},
        {"$push": {"incomes": income_data}}
    )


def update_income_account(username, income_name, updated_data):
    user = userInfo.find_one({"username": username})
    if user:
        incomes = user.get("incomes", [])
        for income in incomes:
            if income["income_name"] == income_name:
                income.update(updated_data)
                break
        userInfo.update_one(
            {"username": username},
            {"$set": {"incomes": incomes}}
        )
    


def delete_income_account(username, income_name):
    userInfo.update_one(
        {"username": username},
        {"$pull": {"incomes": {"income_name": income_name}}}
    )


def get_loan_accounts(username):
    user = userInfo.find_one({"username": username}, {"loans": 1, "_id": 0})
    if user and "loans" in user:
        return user["loans"]
    return []


def save_loan_account(username, loan_data):
    userInfo.update_one(
        {"username": username},
        {"$push": {"loans": loan_data}}
    )


def update_loan_account(username, selected_loan, updated_data):
    user = userInfo.find_one({"username": username})
    if user:
        loans = user.get("loans", [])
        for loan in loans:
            if loan["loan_name"] == selected_loan:
                loan.update(updated_data)
                break
        userInfo.update_one(
            {"username": username},
            {"$set": {"loans": loans}}
        )


def delete_loan_account(username, selected_loan):
    userInfo.update_one(
        {"username": username},
        {"$pull": {"loans": {"loan_name": selected_loan}}}
    )


def get_credit_accounts(username):
    user = userInfo.find_one({"username": username}, {"credit_accounts": 1, "_id": 0})
    if user and "credit_accounts" in user:
        return user["credit_accounts"]
    return []


def save_credit_account(username, credit_data):
    userInfo.update_one(
        {"username": username},
        {"$push": {"credit_accounts": credit_data}}
    )


def update_credit_account(username, selected_credit, updated_data):
    user = userInfo.find_one({"username": username})
    if user:
        credits = user.get("credit_accounts", [])
        for credit in credits:
            if credit["credit_name"] == selected_credit:
                credit.update(updated_data)
                break
        userInfo.update_one(
            {"username": username},
            {"$set": {"credit_accounts": credits}}
        )


def delete_credit_account(username, selected_credit):
    userInfo.update_one(
        {"username": username}, 
        {"$pull": {"credit_accounts": {"credit_name": selected_credit}}}
    )


def get_savings_goals(username):
    user = userInfo.find_one({"username": username}, {"savings_goals": 1, "_id": 0})
    return user.get("savings_goals", []) if user else []


def save_savings_goal(username, goal_data):
    userInfo.update_one({"username": username}, {"$push": {"savings_goals": goal_data}})


def update_savings_goal(username, goal_name, updated_goal_data):
    user = userInfo.find_one({"username": username})
    if user:
        goals = user.get("savings_goals", [])
        for goal in goals:
            if goal["goal_name"] == goal_name:
                goal.update(updated_goal_data)
                break
        userInfo.update_one({"username": username}, {"$set": {"savings_goals": goals}})


def delete_savings_goal(username, goal_name):
    userInfo.update_one({"username": username}, {"$pull": {"savings_goals": {"goal_name": goal_name}}})


def delete_account(username):
    try:
        # Find and delete the user's record
        result = userInfo.delete_one({"username": username})

        if result.deleted_count > 0:
            print(f"User account for '{username}' has been successfully deleted.")
            return True
        else:
            print(f"No account found for the username: '{username}'.")
            return False
    except Exception as e:
        print(f"An error occurred while deleting the account: {e}")
        return False


