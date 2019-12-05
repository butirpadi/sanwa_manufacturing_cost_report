from odoo import api, fields, models


class OperatingExpenseReportConfig(models.Model):
    _name = 'operating.expense.report.config'

    name = fields.Char(
        string='Name', default="Operationg Expenses Report Config")
    net_sales_account_id = fields.Many2one(
        'account.account', string='Net Sales Account')

    payroll_ids = fields.Many2many(
        comodel_name='account.account',
        relation='opr_exp_rep_config_payroll_rel',
        column1='opr_exp_report_id',
        column2='account_id',
        string='Payroll'
    )

    selling_exp_ids = fields.Many2many(
        comodel_name='account.account',
        relation='opr_exp_rep_config_selling_rel',
        column1='opr_exp_report_id',
        column2='account_id',
        string='Payroll'
    )

    administrative_exp_ids = fields.Many2many(
        comodel_name='account.account',
        relation='opr_exp_rep_config_administrative_rel',
        column1='opr_exp_report_id',
        column2='account_id',
        string='Payroll'
    )

    # payroll_ids = fields.One2many(
    #     comodel_name='operating.expense.report.payroll.rel',
    #     inverse_name='opr_exp_report_id',
    #     string='Total of Payroll',
    # )

    # selling_exp_ids = fields.One2many(
    #     comodel_name='operating.expense.report.selling.rel',
    #     inverse_name='opr_exp_report_id',
    #     string='Total of Selling Expenses',
    # )

    # administrative_exp_ids = fields.One2many(
    #     comodel_name='operating.expense.report.administrative.rel',
    #     inverse_name='opr_exp_report_id',
    #     string='Total of Administrative Expenses',
    # )

    def execute(self):
        print('Execute Function')
