from dataclasses import dataclass


@dataclass
class Question:

    question: str
    weight: int


class QuestionEngine:

    def __init__(self):

        self.questions = []

    def add(self, question, weight):

        self.questions.append(
            Question(question, weight)
        )

    def total_weight(self):

        return sum(q.weight for q in self.questions)

    def show(self):

        print("\nQUESTION ENGINE")
        print("-" * 50)

        for i, q in enumerate(self.questions, start=1):

            print(f"{i}. {q.question}   ({q.weight})")