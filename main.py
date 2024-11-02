class InvalidAgeError(Exception):

    def __init__(self, message='Возраст клиента должен быть от 18 до 75 лет'):
        self.message = message
        super().__init__(self.message)


class LoanLimitError(Exception):

    def __init__(self, message='Запрашиваемая сумма превышает лимит'):
        self.message = message
        super().__init__(self.message)


class InvalidRepayment(Exception):

    def __init__(self, message='Погашение не может привышать оставшийся долг'):
        self.message = message
        super().__init__(self.message)


class LoanFountError(Exception):

    def __init__(self, message='Кредит данным ID не найден'):
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
            raise LoanLimitError()
        self.loan_id = loan_id
        self.amount = amount
        self.interest_rate = interest_rate
        self.remaunt_balans = amount

    def make_repayment(self, amount):
        if amount > self.remaunt_balans:
            raise InvalidRepayment()
        self.remaunt_balans -= amount


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
            print(f'Ошибка записи в журнал: {e}')

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
        except LoanLimitError as e:
            message = f'Ошибка при выдаче кредита для {client_name} {e.message}'
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
                raise LoanFountError
            loan.make_repayment(amount)
            message = f'Платёж на сумму {amount} внесён для кредита {loan_id}'
        except LoanFountError as e:
            message = f'Ошибка {e.message}'
            print(message)
        except InvalidRepayment as e:
            message = f'Ошибка при погашении кредита: {e.message}'
            print(message)
        finally:
            self.log_operation(message)


credit_system = CreditSystem()

try:
    client1 = Client('Иванов Иван', 25)
    credit_system.add_client(client1)
except InvalidAgeError as e:
    print(f'Ошибка {e.message}')

try:
    credit_system.issue_loan('Иванов Иван', 'LN001', 30_000, 10)
    credit_system.issue_loan('Иванов Иван', 'LN001', 6_000_000, 10)
except LoanLimitError as e:
    print(f'Ошибка {e.message}')

try:
    credit_system.repay_loan('Иванов Иван', 'LN001', 1000)
    credit_system.repay_loan('Иванов Иван', 'LN001', 40000)
except LoanFountError as e:
    print(f'Ошибка {e.message}')
except InvalidRepayment as e:
    print(f'Ошибка {e.message}')

try:
    with open('operation_log.txt', 'r', encoding='utf-8') as file:
        print('Содержимое журнала операций')
        print(file.read())
except FileNotFoundError:
    print('Файл журнала не найден')




































