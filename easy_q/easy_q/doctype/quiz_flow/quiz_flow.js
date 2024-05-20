// Copyright (c) 2024, Jagadeesan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Quiz Flow", {
    onload:function (frm) {
        frm.fields_dict["flow_table"].grid.get_field("quiz_question_id").get_query = function (doc, cdt, cdn) {
            var child = locals[cdt][cdn];
            return {
                filters: {
                    quiz_customer_group: frm.doc.quiz_customer_group,
                    quiz_list_name: frm.doc.quiz_list_name,
                },
            };
        };
    }
});