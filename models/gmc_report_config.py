from odoo import api, fields, models


class GmcReportConfig(models.Model):
    _name = 'gmc.report.config'
    _description = 'Config for Gross Manufacturing Cost Report'

    name = fields.Char(
        string='Name', default="Gross Manufacturing Cost Report Config")

    property_valuation = fields.Selection([("manual", "Manual (Periodic)"), (
        "real_time", "Automatic (Perpetual)")], string='Inventory Valuation')
    stock_journal_id = fields.Many2one(
        string='Jurnal Persediaan',
        comodel_name='account.journal',
        ondelete='restrict',
    )
    purchase_journal_id = fields.Many2one(
        string='Jurnal Pembelian',
        comodel_name='account.journal',
        ondelete='restrict',
    )
    adjustment_journal_id = fields.Many2one(
        string='Jurnal Penyesuaian',
        comodel_name='account.journal',
        ondelete='restrict',
    )
    stock_input_account_id = fields.Many2one(
        string='Stock Input Account',
        comodel_name='account.account',
        ondelete='restrict',
    )
    pembelian_material_account_id = fields.Many2one(
        string='Akun Pembelian Material',
        comodel_name='account.account',
        ondelete='restrict',
    )
    persediaan_material_account_id = fields.Many2one(
        string='Akun Persediaan Material',
        comodel_name='account.account',
        ondelete='restrict',
    )

    production_amount_account_id = fields.Many2one(
        string='Production Amount Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    begining_material_stock_account_id = fields.Many2one(
        string='Begining Material Stock Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    material_net_purchased_account_id = fields.Many2one(
        string='Material Net Purchased Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    ending_material_stock_account_id = fields.Many2one(
        string='Ending Material Stock Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    material_adjustment_account_id = fields.Many2one(
        string='Material Adjustment Account',
        comodel_name='account.account',
        ondelete='restrict',
    )
    persediaan_barang_dalam_proses_account_id = fields.Many2one(
        string='Akun Persediaan Dalam Proses',
        comodel_name='account.account',
        ondelete='restrict',
    )
    persediaan_barang_jadi_account_id = fields.Many2one(
        string='Akun Persediaan Barang Jadi',
        comodel_name='account.account',
        ondelete='restrict',
    )

    begining_work_in_process_account_id = fields.Many2one(
        string='Begining Work in Process Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    ending_work_in_process_account_id = fields.Many2one(
        string='Ending Work in Process Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    adjustment_account_id = fields.Many2one(
        string='Adjustment Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    process_cost_account_id = fields.Many2one(
        string='Process Cost Account',
        comodel_name='account.account',
        ondelete='restrict',
    )

    labor_cost_account_ids =  fields.Many2many(
        string='Labor Cost Accounts',
        comodel_name='account.account',
        relation='gmc_labor_cost_account_rel',
        column1='gmc_report_config_id',
        column2='account_id',
    )

    manufacturing_expense_account_ids =  fields.Many2many(
        string='Manufacturing Expense Accounts',
        comodel_name='account.account',
        relation='gmc_manufacturing_expense_account_rel',
        column1='gmc_report_config_id',
        column2='account_id',
    )

    def execute(self):
        print('Execute Function')

