from odoo import api, fields, models


class OperatingExpensePayrollRel(models.TransientModel):
    _name = 'operating.expense.report.payroll.rel'

    opr_exp_report_id = fields.Many2one('operating.expense.report', string='Operating Expenses Report')
    account_id = fields.Many2one(
        'account.account', string="Account", ondelete='cascade',)
    account_value = fields.Float('Account Value')
    account_percent = fields.Float('Percent')
    account_value_a_year = fields.Float('Account Value')
    account_percent_a_year = fields.Float('Percent')
    
