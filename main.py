class InvalidAgeError(Exception):
    def __init__(self, message='Возраст клиента должен быть от от 18 до 75'):
        self.message = message
        super().__init__(self.message)
        

class LoanLimitExceededError(Exception):
    def __init__(self, message='Запрошенная сумма превышает лимит'):
        self.message = message
        super().__init__(self.message)


class InvalidRepaymentError(Exception):
    def __init__(self, message='Погашение не может превышать оставшийся долг'):
        self.message = message
        super().__init__(self.message)


class LoanNotFoundError(Exception):
    def __init__(self, message='Кредит с данными ID не найден'):
        self.message = message
        super().__init__(self.message)


class Client:

    def __init__(self, name, age):
        self.name = name
        if not (18 <= age <= 75):
            raise InvalidAgeError()
        self.age = age
        self.loans = []

    def add_loan(self, loan):
        self.loans.append(loan)


class Loan:

    MAX_AMOUNT = 500_000

    def __init__(self, loan_id, amount, interest_rate):
        if amount > Loan.MAX_AMOUNT:
            raise LoanLimitExceededError()
        self.loan_id = loan_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.remaining_balance = amount

    def make_repayment(self, amount):
        if amount > self.remaining_balance:
            raise InvalidRepaymentError()
        self.remaining_balance -= amount


class CreditSystem:

    def __init__(self):
        self.clients = {}

    def add_client(self, client):
        self.clients[client.name] = client

    def log_operation(self, message):
        try:
            with open('operation_log.txt', 'a', encoding='utf-8') as file:
                file.write(message + '\n')
        except Exception as e:
            print(f'Ошибка записи в журнал {e}')

    def issue_loan(self, client_name, loan_id, amount, interest_rate):
        message = ''
        try:
            if client_name not in self.clients:
                raise ValueError('Клиент не найден')

            client = self.clients[client_name]
            loan = Loan(loan_id, amount, interest_rate)
            client.add_loan(loan)
            message = f'Кредит на сумму {amount} выдан клиенту {client_name}'
            print(message)
        except LoanLimitExceededError as e:
            message = f'Ошибка при выдаче кридита для клиента {client_name} {e.message}'
            print(message)
        except ValueError as e:
            message = f'Ошибка {e}'
            print(message)
        finally:
            self.log_operation(message)

    def repay_loan(self, client_name, loan_id, amount):
        message = ''
        try:
            if client_name not in self.clients:
                raise ValueError('Клиент не найден')

            client = self.clients[client_name]
            loan = next((l for l in client.loans if l.loan_id == loan_id), None)

            if loan is None:
                raise LoanNotFoundError()
            loan.make_repayment(amount)
            message = f'Платёж на сумму {amount} внесён для кредита {loan_id}'
            print(message)
        except LoanNotFoundError as e:
            message = f'Ошибка {e.message}'
            print(message)
        except InvalidRepaymentError as e:
            message = f'Ошибка при погашении кредита {e.message}'
            print(message)
        finally:
            self.log_operation(message)


credit_system = CreditSystem()

try:
    client = Client('Иванов Иван', 25)
    credit_system.add_client(client)
except InvalidAgeError as e:
    print(f'Ошибка {e.message}')

try:
    credit_system.issue_loan('Иванов Иван', 'LN001', 30_000, 10)
    credit_system.issue_loan('Иванов Иван', 'LN002', 600_000, 10)
except LoanLimitExceededError as e:
    print(f'Ошибка {e.message}')

try:
    credit_system.repay_loan('Иванов Иван', 'LN001', 10_000)
    credit_system.repay_loan('Иванов Иван', 'LN001', 40_000)
except LoanNotFoundError as e:
    print(f'Ошибка {e.message}')
except InvalidRepaymentError as e:
    print(f'Ошибка {e.message}')

try:
    with open('operation_log.txt', 'r', encoding='utf-8') as file:
        print('Содержимое журнала операций ')
        print(file.read())
except FileNotFoundError:
    print('Файл журнала не найден')






