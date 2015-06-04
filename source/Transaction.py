
class Transaction:
    def __init__(self, amount, date, memo):
        self.amount = amount
        self.date = date
        self.memo = memo

    def __eq__(self, other):
        assert(isinstance(other, Transaction))
        return self.amount == other.amount and self.date == other.date and self.memo == other.memo


def map_data_to_transaction(data, mapping):
    return Transaction(data[mapping.amount_column_index - 1], data[mapping.date_column_index - 1],
                       data[mapping.memo_column_index - 1])
