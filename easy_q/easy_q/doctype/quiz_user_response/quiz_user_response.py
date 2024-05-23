# Copyright (c) 2024, Jagadeesan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class QuizUserResponse(Document):
    def validate(self):
        option_map = {
            1: "First Option",
            2: "Second Option",
            3: "Third Option",
            4: "Fourth Option",
            5: "Fifth Option",
            6: "Sixth Option"
        }

        if self.quiz_completed_status == 1:
            quiz_score_cards = frappe.db.get_all("Quiz Score Card", filters={"quiz_group": self.quiz_group},fields=["*"])
            for quiz_score in quiz_score_cards:
                score_card_table = frappe.db.get_all("Quiz Score Card Table", filters={"parent": quiz_score.name}, fields=["quiz_question_id", "quiz_option"])                
                for user_response in self.response_table:
                    match_found = False
                    user_response_quiz_question_id = user_response.quiz_question_id
                    user_response_quiz_option = option_map.get(int(user_response.response_option))
                    
                    for score_card in score_card_table:
                        if user_response_quiz_question_id == score_card.quiz_question_id and user_response_quiz_option == score_card.quiz_option:
                            match_found = True
                            break

                    # if not match_found:
                    #     frappe.throw(f"No matching entry found for Question ID {user_response_quiz_question_id} with Option {user_response_quiz_option} in Score Card Table.")
                
                for score_card in score_card_table:
                    match_found = False
                    score_card_question_id = score_card.quiz_question_id
                    score_card_option = score_card.quiz_option
                    
                    for user_response in self.response_table:
                        if score_card_question_id == user_response.quiz_question_id and score_card_option == option_map.get(int(user_response.response_option)):
                            match_found = True
                            break

                    if not match_found:
                        frappe.throw(f"No matching entry found for Question ID {score_card_question_id} with Option {score_card_option} in User Response Table.")

                for user_response in self.response_table:
                    user_response_question_id = user_response.quiz_question_id
                    user_response_option = option_map.get(int(user_response.response_option))
                    
                    for score_card in score_card_table:
                        if user_response_question_id == score_card.quiz_question_id and user_response_option == score_card.quiz_option:
                            self.append("quiz_score_card", {
                                "quiz_question_id": user_response_question_id,
                                "quiz_option": user_response_option,
                            })
                            self.score_review_statement = quiz_score.quiz_question_based_statement

                # frappe.msgprint("All entries in User Response Table match with Score Card Table.")

