class InvalidAgeError(Exception):

    def __init__(self, massage='Возраст клиента должен быть от 18 до 75 лет'):
        self.massage = massage
        super().__init__(self.massage)


class LoanLimitError(Exception):

    def __init__(self, massage='Запрашиваемая сумма превышает лимит'):
        self.massage = massage
        super().__init__(self.massage)


class InvalidRepayment(Exception):

    def __init__(self, massage='Погашение не может привышать оставшийся долг'):
        self.massage = massage
        super().__init__(self.massage)


class LoanFountError(Exception):

    def __init__(self, massage='Кредит данным ID не найден'):
        self.massage = massage
        super().__init__(self.massage)


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

    MAX_AMOUNT = 500000

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

    def log_operation(self, massage):
        try:
            with open('operation_log.txt', 'a', encoding='utf-8') as file:
                file.write(massage + '\n')
        except Exception as e:
            print(f'Ошибка записи в журнал: {e}')

    def issue_loan(self, client_name, loan_id, amount, interest_rate):
        massage = ''
        try:
            if client_name not in self.clients:
                raise ValueError('Клиент не найден')

            client = self.clients[client_name]
            loan = Loan(loan_id, amount, interest_rate)
            client.add_loan(loan)
            massage = f'Кредит на сумму {amount} выдан клиенту {client_name}'
            print(massage)
        except LoanLimitError as e:
            massage = f'Оштбка при выдаче кредита для {client_name} {e.massage}'
            print(massage)
        except ValueError as e:
            massage = f'Ошибка {e}'
            print(massage)
        finally:
            self.log_operation(massage)


    def repay_loan(self, client_name, loan_id, amount):
        massage = ''
        try:
            if client_name not in self.clients:
                raise ValueError('Клиент не найден')

            client = self.clients[client_name]
            loan = next((l for l in client.loans if l.loan_id == loan_id), None)
            if loan is None:
                raise LoanFountError
            loan.make_repayment(amount)
            massage = f'Платёж на сумму {amount} внесён для кредита {loan_id}'
        except LoanFountError as e:
            massage = f'Ошибка {e.massage}'
            print(massage)
        except InvalidRepayment as e:
            massage = f'Ошибка при погашении кредита: {e.massage}'
            print(massage)
        finally:
            self.log_operation(massage)


credit_system = CreditSystem()

try:
    client1 = Client('Иванов Иван', 25)
    credit_system.add_client(client1)
except InvalidAgeError as e:
    print(f'Ошибка {e.massage}')

try:
    credit_system.issue_loan('Иванов Иван', 'LN001', 30000, 10)
    credit_system.issue_loan('Иванов Иван', 'LN001', 6000000, 10)
except LoanLimitError as e:
    print(f'Ошибка {e.massage}')

try:
    credit_system.repay_loan('Иванов Иван', 'LN001', 1000)
    credit_system.repay_loan('Иванов Иван', 'LN001', 40000)
except LoanFountError as e:
    print(f'Ошибка {e.massage}')
except InvalidRepayment as e:
    print(f'Ошибка {e.massage}')

try:
    with open('operation_log.txt', 'r', encoding='utf-8') as file:
        print('Содержимое журнала операций')
        print(file.read())
except FileNotFoundError:
    print('Файл журнала не найден')




































