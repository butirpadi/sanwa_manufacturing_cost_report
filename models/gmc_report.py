from odoo import fields, models, api, _
from odoo.exceptions import UserError
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta


class GmcReport(models.TransientModel):
    _name = 'gmc.report'
    _description = 'Gross Manufacture Report'

    name = fields.Char(string='Name', default="Gross Manufacture Cost Report")
    date_from = fields.Date(string="Date start")
    date_to = fields.Date(string="Date to")

    production_amount_account_id = fields.Many2one(
        string='Production Amount Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    production_amount = fields.Float(string="Production Amount")
    production_amount_a_year = fields.Float(string="Production Amount")

    cost_of_material_used_amount = fields.Float(
        string="Cost of Material Used Amount")
    cost_of_material_used_amount_percent = fields.Float(
        string="Cost of Material Used Amount Percent")

    cost_of_material_used_amount_a_year = fields.Float(
        string="Cost of Material Used Amount")
    cost_of_material_used_amount_percent_a_year = fields.Float(
        string="Cost of Material Used Amount Percent")

    begining_material_stock_account_id = fields.Many2one(
        string='Begining Material Stock Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    begining_material_stock = fields.Float(string="Begining Material Stock")
    begining_material_stock_percent = fields.Float(
        string="Begining Material Stock Percent")

    begining_material_stock_a_year = fields.Float(
        string="Begining Material Stock")
    begining_material_stock_percent_a_year = fields.Float(
        string="Begining Material Stock Percent")

    material_net_purchased_account_id = fields.Many2one(
        string='Material Net Purchased Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    material_net_purchased = fields.Float(string="Materials Net Purchased")
    material_net_purchased_percent = fields.Float(
        string="Materials Net Purchased Percent")

    material_net_purchased_a_year = fields.Float(
        string="Materials Net Purchased")
    material_net_purchased_percent_a_year = fields.Float(
        string="Materials Net Purchased Percent")

    ending_material_stock_account_id = fields.Many2one(
        string='Ending Material Stock Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    ending_material_stock = fields.Float(string="Ending Material Stock")
    ending_material_stock_percent = fields.Float(
        string="Ending Material Stock Percent")

    ending_material_stock_a_year = fields.Float(string="Ending Material Stock")
    ending_material_stock_percent_a_year = fields.Float(
        string="Ending Material Stock Percent")

    material_adjustment_account_id = fields.Many2one(
        string='Material Adjustment Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    material_adjustment = fields.Float(string="Material Adjustments ETC")
    material_adjustment_percent = fields.Float(
        string="Material Adjustments ETC Percent")

    material_adjustment_a_year = fields.Float(
        string="Material Adjustments ETC")
    material_adjustment_percent_a_year = fields.Float(
        string="Material Adjustments ETC Percent")

    begining_work_in_process_account_id = fields.Many2one(
        string='Begining Work in Process Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    begining_work_in_process = fields.Float(string="Begining Work in Process")
    begining_work_in_process_percent = fields.Float(
        string="Begining Work in Process Percent")

    begining_work_in_process_a_year = fields.Float(
        string="Begining Work in Process")
    begining_work_in_process_percent_a_year = fields.Float(
        string="Begining Work in Process Percent")

    ending_work_in_process_account_id = fields.Many2one(
        string='Ending Work in Process Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    ending_work_in_process = fields.Float(string="Ending Work in Process")
    ending_work_in_process_percent = fields.Float(
        string="Ending Work in Process Percent")

    ending_work_in_process_a_year = fields.Float(
        string="Ending Work in Process")
    ending_work_in_process_percent_a_year = fields.Float(
        string="Ending Work in Process Percent")

    adjustment_account_id = fields.Many2one(
        string='Adjustment Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    adjustment = fields.Float(string="Adjustments")
    adjustment_percent = fields.Float(string="Adjustments Percent")

    adjustment_a_year = fields.Float(string="Adjustments")
    adjustment_percent_a_year = fields.Float(string="Adjustments Percent")

    process_cost_account_id = fields.Many2one(
        string='Process Cost Account',
        comodel_name='account.account',
        ondelete='cascade',
    )
    process_cost = fields.Float(string="Process Cost")
    process_cost_percent = fields.Float(string="Process Cost Percent")

    process_cost_a_year = fields.Float(string="Process Cost")
    process_cost_percent_a_year = fields.Float(string="Process Cost Percent")

    labor_cost = fields.One2many(
        string='Labor Cost',
        comodel_name='gmc.report.labor.cost.rel',
        inverse_name='gmc_report_id',
    )
    labor_cost_amount = fields.Float(string="Labor Cost Amount")
    labor_cost_amount_percent = fields.Float(
        string="Labor Cost Amount Percent")

    labor_cost_amount_a_year = fields.Float(string="Labor Cost Amount")
    labor_cost_amount_percent_a_year = fields.Float(
        string="Labor Cost Amount Percent")

    manufacture_expenses = fields.One2many(
        string='Labor Cost',
        comodel_name='gmc.report.manufacture.expense.rel',
        inverse_name='gmc_report_id',
    )
    manufacture_expenses_amount = fields.Float(
        string="Manufacturing Expenses Amount")
    manufacture_expenses_amount_percent = fields.Float(
        string="Manufacturing Expenses Amount Percent")

    manufacture_expenses_amount_a_year = fields.Float(
        string="Manufacturing Expenses Amount")
    manufacture_expenses_amount_percent_a_year = fields.Float(
        string="Manufacturing Expenses Amount Percent")

    def action_submit(self):
        begining_mat_value = 0
        purch_mat_value = 0
        adjust_mat_value = 0
        total_raw_return = 0
        total_consumed = 0
        ending_mat_value = 0
        ending_comp_value = 0
        total_mat_cost = 0
        labor_cost = 0
        overhead_cost = 0
        begining_wip = 0
        ending_wip = 0
        total_wip = 0
        begining_goods = 0
        ending_goods = 0
        total_goods = 0
        total_production_cost = 0

        payable_type = self.env.ref('account.data_account_type_payable')
        payable_accounts = self.env['account.account'].search(
            [('user_type_id', '=', payable_type.id)])

        report_config = self.env.ref(
            'sanwa_manufacturing_cost_report.gmc_report_config_default')
        akun_persediaan = report_config.persediaan_material_account_id
        akun_pembelian = report_config.pembelian_material_account_id
        stock_input_akun = report_config.stock_input_account_id

        akun_persediaan_wip = report_config.persediaan_barang_dalam_proses_account_id
        akun_persediaan_jadi = report_config.persediaan_barang_jadi_account_id

        stock_journal = report_config.stock_journal_id
        purchase_journal = report_config.purchase_journal_id
        adjustment_journal = report_config.adjustment_journal_id

        # # get material value
        # begin_mat = self.env['account.move.line'].search(
        #     [('account_id', '=', akun_persediaan.id), ('date', '<', self.date_from)])
        # begin_mat = begin_mat.filtered(lambda x: x.move_id.state == 'posted')
        # begining_mat_value = sum(begin_mat.mapped('balance'))

        # # get purchased material
        # if report_config.property_valuation == 'manual':
        #     purch_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&', '&',
        #             ('account_id', '=', akun_pembelian.id),
        #             ('date', '>=', self.date_from),
        #             ('date', '<=', self.date_to),
        #             ('debit', '>', 0),
        #             ('journal_id', '=', purchase_journal.id)])
        #     purch_aml.filtered(lambda ml: ml.move_id.state == 'posted')

        #     purch_mat_value = sum(purch_aml.mapped('debit'))

        # else:

        #     purch_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&',
        #         ('account_id', '=', akun_persediaan.id),
        #         ('date', '>=', self.date_from),
        #         ('date', '<=', self.date_to), ('debit', '>', 0),
        #         ('journal_id', '=', stock_journal.id),
        #         ])
        #     purch_aml.filtered(lambda ml: ml.move_id.state == 'posted')
        #     purch_mat_value = sum(purch_aml.mapped('debit'))

        # # get adjustment
        # if report_config.property_valuation == 'manual':
        #     adjust_aml = self.env['account.move.line'].search(
        #         ['&', '&',
        #          ('account_id', '=', akun_pembelian.id),
        #          ('date', '>=', self.date_from),
        #          ('date', '<=', self.date_to),
        #          ('journal_id', '=', adjustment_journal.id)
        #          ])
        #     adjust_aml.filtered(lambda ml: ml.move_id.state == 'posted')
        #     adjust_mat_value = sum(adjust_aml.mapped('balance'))
        # else:
        #     adjust_aml = self.env['account.move.line'].search(
        #         ['&', '&',
        #         ('account_id', '=', akun_persediaan.id),
        #         ('date', '>=', self.date_from),
        #         ('date', '<=', self.date_to),
        #         ('journal_id', '=', adjustment_journal.id)
        #         ])
        #     adjust_aml.filtered(lambda ml: ml.move_id.state == 'posted')
        #     adjust_mat_value = sum(adjust_aml.mapped('balance'))

        # # get retur move
        # if report_config.property_valuation == 'manual':
        #     payable_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&', ('account_id', 'in', payable_accounts.ids), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('debit', '>', 0)])
        #     payable_move = payable_aml.mapped('move_id')
        #     payable_move = payable_move.filtered(
        #         lambda mv: akun_pembelian.id in mv.line_ids.mapped('account_id').ids)
        #     payable_move = payable_move.filtered(
        #         lambda mv: mv.state == 'posted')
        #     fix_payable_aml = payable_move.mapped('line_ids')
        #     fix_payable_aml = fix_payable_aml.filtered(
        #         lambda ln: ln.account_id.id == akun_pembelian.id and ln.credit > 0)
        #     total_raw_return = sum(fix_payable_aml.mapped('credit'))
        # else:
        #     return_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&', ('account_id', '=', akun_persediaan.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('credit', '>', 0)])
        #     return_move = return_aml.mapped('move_id')
        #     return_move = return_move.filtered(
        #         lambda mv: stock_input_akun.id in mv.line_ids.mapped('account_id').ids)
        #     return_move = return_move.filtered(lambda mv: mv.state == 'posted')
        #     fix_return_aml = return_move.mapped('line_ids')
        #     fix_return_aml = fix_return_aml.filtered(
        #         lambda ln: ln.account_id.id == akun_persediaan.id and ln.credit > 0)
        #     total_raw_return = sum(fix_return_aml.mapped('credit'))

        # ending_mat = self.env['account.move.line'].search(
        #     [('account_id', '=', akun_persediaan.id), ('date', '<=', self.date_to)])
        # ending_mat = ending_mat.filtered(lambda x: x.move_id.state == 'posted')
        # ending_mat_value = sum(ending_mat.mapped('balance'))

        # total_mat_cost = begining_mat_value + purch_mat_value + \
        #     adjust_mat_value - total_raw_return - ending_mat_value

        # # ----------------------------------------------------------------------------------------
        # # get labor cost
        # labor_accounts = report_config.labor_cost_account_ids
        # labor_cost = {}
        # labor_cost_value = 0

        # lbr_aml = self.env['account.move.line'].search([
        #     ('account_id', 'in', labor_accounts.ids),
        #     ('date', '>=', self.date_from),
        #     ('date', '<=', self.date_to)
        # ])
        # lbr_aml = lbr_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        # labor_cost_value = abs(sum(lbr_aml.mapped('balance')))

        # for acc in labor_accounts:
        #     acc_amls = self.env['account.move.line'].search(
        #         ['&', '&',
        #          ('account_id', '=', acc.id),
        #             ('date', '>=', self.date_from),
        #             ('date', '<=', self.date_to)
        #          ])
        #     acc_amls = acc_amls.filtered(
        #         lambda ac: ac.move_id.state == 'posted')
        #     total_amls = abs(sum(acc_amls.mapped('balance')))
        #     if(total_amls > 0):
        #         labor_cost[acc] = total_amls

        # # ----------------------------------------------------------------------------------------
        # # get production cost
        # overhead_cost_accounts = report_config.overhead_cost_account_ids
        # overhead_cost = {}
        # overhead_cost_value = 0

        # ovh_aml = self.env['account.move.line'].search([
        #     ('account_id', 'in', overhead_cost_accounts.ids),
        #     ('date', '>=', self.date_from),
        #     ('date', '<=', self.date_to)
        # ])
        # ovh_aml = ovh_aml.filtered(lambda ac: ac.move_id.state == 'posted')
        # overhead_cost_value = abs(sum(ovh_aml.mapped('balance')))

        # for acc in overhead_cost_accounts:
        #     acc_amls = self.env['account.move.line'].search(
        #         ['&', '&',
        #          ('account_id', '=', acc.id),
        #             ('date', '>=', self.date_from),
        #             ('date', '<=', self.date_to)
        #          ])
        #     acc_amls = acc_amls.filtered(
        #         lambda ac: ac.move_id.state == 'posted')
        #     total_amls = abs(sum(acc_amls.mapped('balance')))
        #     if(total_amls > 0):
        #         overhead_cost[acc] = total_amls

        # total_production_cost = total_mat_cost + overhead_cost_value + labor_cost_value
        # cost_of_material_used_amount = total_production_cost

        # # ----------------------------------------------------------------------------------------
        # # get WIP
        # begining_wip_aml = self.env['account.move.line'].search(
        #     [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
        #      ('date', '<', self.date_from)
        #      ])
        # begining_wip_aml = begining_wip_aml.filtered(
        #     lambda x: x.move_id.state == 'posted')
        # begining_wip = sum(begining_wip_aml.mapped('balance'))

        # ending_wip_aml = self.env['account.move.line'].search(
        #     [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
        #      ('date', '<=', self.date_to)
        #      ])
        # ending_wip_aml = ending_wip_aml.filtered(
        #     lambda x: x.move_id.state == 'posted')
        # ending_wip = sum(ending_wip_aml.mapped('balance'))
        # total_wip = begining_wip + total_production_cost - ending_wip

        # # ----------------------------------------------------------------------------------------
        # # Get Goods
        # begining_goods_aml = self.env['account.move.line'].search(
        #     [('account_id', '=', report_config.persediaan_barang_jadi_account_id.id),
        #      ('date', '<', self.date_from)
        #      ])
        # begining_goods_aml = begining_goods_aml.filtered(
        #     lambda x: x.move_id.state == 'posted')
        # begining_goods = sum(begining_goods_aml.mapped('balance'))

        # ending_goods_aml = self.env['account.move.line'].search(
        #     [('account_id', '=', report_config.persediaan_barang_jadi_account_id.id),
        #      ('date', '<=', self.date_to)
        #      ])
        # ending_goods_aml = ending_goods_aml.filtered(
        #     lambda x: x.move_id.state == 'posted')
        # ending_goods = sum(ending_goods_aml.mapped('balance'))

        # total_goods = begining_goods + total_production_cost - ending_goods

        # get report setting
        gmc_report_config = self.env['gmc.report.config'].search([], limit=1)

        # get one year
        current_year = datetime(self.date_from.year, self.env.user.company_id.fiscalyear_last_month,
                                self.env.user.company_id.fiscalyear_last_day, 0, 0, 0)
        delta = relativedelta(months=12)
        # year_to_date = current_year - delta # satu tahun lalu
        # year_to_date diartikan sejauh tahun ini, jadi di ambil awal tahun ini 1 januari.
        year_to_date = datetime(self.date_from.year, 1,
                                1, 0, 0, 0)  # deprecated
        # replace year_to_date dengan nama lain
        first_date_of_this_year = datetime(self.date_from.year, 1, 1, 0, 0, 0)

        self.production_amount_account_id = gmc_report_config.production_amount_account_id.id
        self.begining_material_stock_account_id = gmc_report_config.begining_material_stock_account_id.id
        self.material_net_purchased_account_id = gmc_report_config.material_net_purchased_account_id.id
        self.ending_material_stock_account_id = gmc_report_config.ending_material_stock_account_id.id
        self.material_adjustment_account_id = gmc_report_config.material_adjustment_account_id.id
        self.begining_work_in_process_account_id = gmc_report_config.begining_work_in_process_account_id.id
        self.ending_work_in_process_account_id = gmc_report_config.ending_work_in_process_account_id.id
        self.adjustment_account_id = gmc_report_config.adjustment_account_id.id
        self.process_cost_account_id = gmc_report_config.process_cost_account_id.id

        # get amount of production_amount
        prd_amt = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.production_amount_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.production_amount = sum(prd_amt.mapped(
            'debit')) - sum(prd_amt.mapped('credit'))

        prd_amt_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.production_amount_account_id.id),
                ('date_maturity', '>', year_to_date),
                ('date_maturity', '<=', current_year)
             ])

        self.production_amount_a_year = sum(prd_amt_a_year.mapped(
            'debit')) - sum(prd_amt_a_year.mapped('credit'))

        # get amount of begining_material_stock
        # bgn_mat_stk = self.env['account.move.line'].search(
        #     ['&', '&',
        #         ('account_id', '=', self.begining_material_stock_account_id.id),
        #         ('date_maturity', '>=', self.date_from),
        #         ('date_maturity', '<=', self.date_to)
        #      ])

        # self.begining_material_stock = sum(bgn_mat_stk.mapped(
        #     'debit')) - sum(bgn_mat_stk.mapped('credit'))

        #  BEGINING MATERIAL STOCK
        begin_mat = self.env['account.move.line'].search(
            [('account_id', '=', akun_persediaan.id), ('date', '<', self.date_from)])
        begin_mat = begin_mat.filtered(lambda x: x.move_id.state == 'posted')
        begining_mat_value = sum(begin_mat.mapped('balance'))
        self.begining_material_stock = begining_mat_value

        if self.production_amount > 0:
            self.begining_material_stock_percent = self.begining_material_stock / \
                self.production_amount * 100
        else:
            self.begining_material_stock_percent = 0.0

        begin_mat_a_year = self.env['account.move.line'].search(
            [('account_id', '=', akun_persediaan.id),
                ('date', '<', first_date_of_this_year)
             ])
        begin_mat_a_year = begin_mat_a_year.filtered(
            lambda x: x.move_id.state == 'posted')
        begining_mat_a_year_value = sum(begin_mat_a_year.mapped('balance'))
        self.begining_material_stock_a_year = begining_mat_a_year_value

        if self.production_amount_a_year > 0:
            self.begining_material_stock_percent_a_year = self.begining_material_stock_a_year / \
                self.production_amount_a_year * 100
        else:
            self.begining_material_stock_percent_a_year = 0.0
        # ---------------------------------------------------------------------------

        # GET NET MATERIAL PURCHASED
        if report_config.property_valuation == 'manual':
            purch_aml = self.env['account.move.line'].search(
                ['&', '&', '&', '&',
                    ('account_id', '=', akun_pembelian.id),
                    ('date', '>=', self.date_from),
                    ('date', '<=', self.date_to),
                    ('debit', '>', 0),
                    ('journal_id', '=', purchase_journal.id)])
            purch_aml.filtered(lambda ml: ml.move_id.state == 'posted')

            purch_mat_value = sum(purch_aml.mapped('debit'))

        else:
            purch_aml = self.env['account.move.line'].search(
                ['&', '&', '&',
                 ('account_id', '=', akun_persediaan.id),
                 ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to), ('debit', '>', 0),
                 ('journal_id', '=', stock_journal.id),
                 ])
            purch_aml.filtered(lambda ml: ml.move_id.state == 'posted')
            purch_mat_value = sum(purch_aml.mapped('debit'))

        self.material_net_purchased = purch_mat_value

        if self.production_amount > 0:
            self.material_net_purchased_percent = self.material_net_purchased / \
                self.production_amount * 100
        else:
            self.material_net_purchased_percent = 0.0

        if report_config.property_valuation == 'manual':
            purch_aml_a_year = self.env['account.move.line'].search(
                ['&', '&', '&', '&',
                    ('account_id', '=', akun_pembelian.id),
                    # sepanjang tahun ini artinya, awal tahun sampai akhir tanggal yang di tentukan di wizard
                    ('date', '>=', first_date_of_this_year),
                    ('date', '<=', self.date_to),
                    ('debit', '>', 0),
                    ('journal_id', '=', purchase_journal.id)])
            purch_aml_a_year.filtered(lambda ml: ml.move_id.state == 'posted')

            purch_mat_value_a_year = sum(purch_aml_a_year.mapped('debit'))

        else:
            purch_aml_a_year = self.env['account.move.line'].search(
                ['&', '&', '&',
                    ('account_id', '=', akun_persediaan.id),
                    ('date', '>=', first_date_of_this_year),
                    ('date', '<=', self.date_to),
                    ('debit', '>', 0),
                    ('journal_id', '=', stock_journal.id),
                 ])
            purch_aml_a_year.filtered(lambda ml: ml.move_id.state == 'posted')
            purch_mat_value_a_year = sum(purch_aml_a_year.mapped('debit'))

        self.material_net_purchased_a_year = purch_mat_value_a_year

        if self.production_amount_a_year > 0:
            self.material_net_purchased_percent_a_year = self.material_net_purchased_a_year / \
                self.production_amount_a_year * 100
        else:
            self.material_net_purchased_percent_a_year = 0
        # ---------------------------------------------------------------------------

        # bgn_mat_stk_a_year = self.env['account.move.line'].search(
        #     ['&', '&',
        #         ('account_id', '=', self.begining_material_stock_account_id.id),
        #         ('date_maturity', '>', year_to_date),
        #         ('date_maturity', '<=', current_year)
        #      ])

        # self.begining_material_stock_a_year = sum(bgn_mat_stk_a_year.mapped(
        #     'debit')) - sum(bgn_mat_stk_a_year.mapped('credit'))

        # get amount of material_net_purchased

        # mat_net_purch = self.env['account.move.line'].search(
        #     ['&', '&',
        #         ('account_id', '=', self.material_net_purchased_account_id.id),
        #         ('date_maturity', '>=', self.date_from),
        #         ('date_maturity', '<=', self.date_to)
        #      ])

        # self.material_net_purchased = sum(mat_net_purch.mapped(
        #     'debit')) - sum(mat_net_purch.mapped('credit'))

        # mat_net_purch_a_year = self.env['account.move.line'].search(
        #     ['&', '&',
        #         ('account_id', '=', self.material_net_purchased_account_id.id),
        #         ('date_maturity', '>', year_to_date),
        #         ('date_maturity', '<=', current_year)
        #      ])

        # self.material_net_purchased_a_year = sum(mat_net_purch_a_year.mapped(
        #     'debit')) - sum(mat_net_purch_a_year.mapped('credit'))

        # end_mat_stk = self.env['account.move.line'].search(
        #     ['&', '&',
        #         ('account_id', '=', self.ending_material_stock_account_id.id),
        #         ('date_maturity', '>=', self.date_from),
        #         ('date_maturity', '<=', self.date_to)
        #      ])

        # self.ending_material_stock = sum(end_mat_stk.mapped(
        #     'debit')) - sum(end_mat_stk.mapped('credit'))

        # end_mat_stk_a_year = self.env['account.move.line'].search(
        #     ['&', '&',
        #         ('account_id', '=', self.ending_material_stock_account_id.id),
        #         ('date_maturity', '>', year_to_date),
        #         ('date_maturity', '<=', current_year)
        #      ])

        # self.ending_material_stock_a_year = sum(end_mat_stk_a_year.mapped(
        #     'debit')) - sum(end_mat_stk_a_year.mapped('credit'))

        # GET ENDING MATERIAL STOCK
        ending_mat = self.env['account.move.line'].search(
            [('account_id', '=', akun_persediaan.id), 
            ('date', '<=', self.date_to)])
        ending_mat = ending_mat.filtered(lambda x: x.move_id.state == 'posted')
        print('ENDING MATERIAL DEBIT : ' + str(sum(ending_mat.mapped('debit'))))
        print('ENDING MATERIAL CREDIT : ' + str(sum(ending_mat.mapped('credit'))))
        print('ENDING MATERIAL BALANCE : ' + str(sum(ending_mat.mapped('balance'))))
        ending_mat_value = sum(ending_mat.mapped('balance'))
        self.ending_material_stock = ending_mat_value

        if self.production_amount > 0:
            self.ending_material_stock_percent = self.ending_material_stock / \
                self.production_amount * 100
        else:
            self.ending_material_stock_percent = 0.0

        self.ending_material_stock_a_year = ending_mat_value

        if self.production_amount_a_year > 0:
            self.ending_material_stock_percent_a_year = self.ending_material_stock_a_year / \
                self.production_amount_a_year * 100
        else:
            self.ending_material_stock_percent_a_year = 0
        # ---------------------------------------------------------------------------

        # # GET MATERIALS ADJUSTMENT
        # if report_config.property_valuation == 'manual':
        #     adjust_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&',
        #          ('account_id', '=', akun_pembelian.id),
        #          ('date', '>=', self.date_from),
        #          ('date', '<=', self.date_to),
        #          ('journal_id', '=', adjustment_journal.id)
        #          ])
        #     adjust_aml.filtered(lambda ml: ml.move_id.state == 'posted')
        #     adjust_mat_value = sum(adjust_aml.mapped('balance'))
        # else:
        #     adjust_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&',
        #          ('account_id', '=', akun_persediaan.id),
        #          ('date', '>=', self.date_from),
        #          ('date', '<=', self.date_to),
        #          ('journal_id', '=', adjustment_journal.id)
        #          ])
        #     adjust_aml.filtered(lambda ml: ml.move_id.state == 'posted')
        #     adjust_mat_value = sum(adjust_aml.mapped('balance'))

        # self.material_adjustment = adjust_mat_value

        # if report_config.property_valuation == 'manual':
        #     adjust_aml_a_year = self.env['account.move.line'].search(
        #         ['&', '&', '&',
        #          ('account_id', '=', akun_pembelian.id),
        #          ('date', '>=', first_date_of_this_year),
        #          ('date', '<=', self.date_to),
        #          ('journal_id', '=', adjustment_journal.id)
        #          ])
        #     adjust_aml_a_year.filtered(lambda ml: ml.move_id.state == 'posted')
        #     adjust_mat_value_a_year = sum(adjust_aml_a_year.mapped('balance'))
        # else:
        #     adjust_aml_a_year = self.env['account.move.line'].search(
        #         ['&', '&', '&',
        #          ('account_id', '=', akun_persediaan.id),
        #          ('date', '>=', first_date_of_this_year),
        #          ('date', '<=', self.date_to),
        #          ('journal_id', '=', adjustment_journal.id)
        #          ])
        #     adjust_aml_a_year.filtered(lambda ml: ml.move_id.state == 'posted')
        #     adjust_mat_value_a_year = sum(adjust_aml_a_year.mapped('balance'))

        # self.material_adjustment_a_year = adjust_mat_value_a_year

        # # GET RETURN MOVE
        # if report_config.property_valuation == 'manual':
        #     payable_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&', '&',
        #             ('account_id', 'in', payable_accounts.ids),
        #             ('date', '>=', self.date_from),
        #             ('date', '<=', self.date_to),
        #             ('debit', '>', 0),
        #             ('journal_id', '=', purchase_journal.id)
        #          ])
        #     payable_move = payable_aml.mapped('move_id')
        #     payable_move = payable_move.filtered(
        #         lambda mv: akun_pembelian.id in mv.line_ids.mapped('account_id').ids)
        #     payable_move = payable_move.filtered(
        #         lambda mv: mv.state == 'posted')
        #     fix_payable_aml = payable_move.mapped('line_ids')
        #     fix_payable_aml = fix_payable_aml.filtered(
        #         lambda ln: ln.account_id.id == akun_pembelian.id)
        #     total_raw_return = sum(fix_payable_aml.mapped('credit'))
        # else:
        #     return_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&', '&',
        #             ('account_id', '=', akun_persediaan.id),
        #             ('date', '>=', self.date_from),
        #             ('date', '<=', self.date_to),
        #             ('credit', '>', 0),
        #             ('journal_id', '=', stock_journal.id)
        #          ])
        #     return_move = return_aml.mapped('move_id')
        #     return_move = return_move.filtered(
        #         lambda mv: stock_input_akun.id in mv.line_ids.mapped('account_id').ids)
        #     return_move = return_move.filtered(lambda mv: mv.state == 'posted')
        #     fix_return_aml = return_move.mapped('line_ids')
        #     fix_return_aml = fix_return_aml.filtered(
        #         lambda ln: ln.account_id.id == akun_persediaan.id)
        #     total_raw_return = sum(fix_return_aml.mapped('credit'))

        # self.material_adjustment += total_raw_return

        # total_raw_return_a_year = 0
        # if report_config.property_valuation == 'manual':
        #     payable_aml_a_year = self.env['account.move.line'].search(
        #         ['&', '&', '&', '&',
        #             ('account_id', 'in', payable_accounts.ids),
        #             ('date', '>=', first_date_of_this_year),
        #             ('date', '<=', self.date_to),
        #             ('debit', '>', 0),
        #             ('journal_id', '=', purchase_journal.id)
        #          ])
        #     payable_move = payable_aml_a_year.mapped('move_id')
        #     payable_move = payable_move.filtered(
        #         lambda mv: akun_pembelian.id in mv.line_ids.mapped('account_id').ids)
        #     payable_move = payable_move.filtered(
        #         lambda mv: mv.state == 'posted')
        #     fix_payable_aml = payable_move.mapped('line_ids')
        #     fix_payable_aml = fix_payable_aml.filtered(
        #         lambda ln: ln.account_id.id == akun_pembelian.id)
        #     total_raw_return_a_year = sum(fix_payable_aml.mapped('credit'))
        # else:
        #     return_aml = self.env['account.move.line'].search(
        #         ['&', '&', '&', '&',
        #             ('account_id', '=', akun_persediaan.id),
        #             ('date', '>=', first_date_of_this_year),
        #             ('date', '<=', self.date_to),
        #             ('credit', '>', 0),
        #             ('journal_id', '=', stock_journal.id)
        #          ])
        #     return_move = return_aml.mapped('move_id')
        #     return_move = return_move.filtered(
        #         lambda mv: stock_input_akun.id in mv.line_ids.mapped('account_id').ids)
        #     return_move = return_move.filtered(lambda mv: mv.state == 'posted')
        #     fix_return_aml = return_move.mapped('line_ids')
        #     fix_return_aml = fix_return_aml.filtered(
        #         lambda ln: ln.account_id.id == akun_persediaan.id)
        #     total_raw_return_a_year = sum(fix_return_aml.mapped('credit'))

        # self.material_adjustment_a_year += total_raw_return_a_year

        # if self.production_amount > 0:
        #     self.material_adjustment_percent = self.material_adjustment / \
        #         self.production_amount * 100
        # else:
        #     self.material_adjustment_percent = 0.0

        # if self.production_amount_a_year > 0:
        #     self.material_adjustment_percent_a_year = self.material_adjustment_a_year / \
        #         self.production_amount_a_year * 100
        # else:
        #     self.material_adjustment_percent_a_year = 0
        # # ---------------------------------------------------------------------------

        # GET BEGINING WORK IN PROCESS WIP
        begining_wip_aml = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
             ('date', '<', self.date_from)
             ])
        begining_wip_aml = begining_wip_aml.filtered(
            lambda x: x.move_id.state == 'posted')
        begining_wip = sum(begining_wip_aml.mapped('balance'))
        self.begining_work_in_process = begining_wip

        if self.production_amount > 0:
            self.begining_work_in_process_percent = self.begining_work_in_process / \
                self.production_amount * 100
        else:
            self.begining_work_in_process_percent = 0.0

        begining_wip_aml_A_YEAR = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
             ('date', '<', first_date_of_this_year)
             ])
        begining_wip_aml_A_YEAR = begining_wip_aml_A_YEAR.filtered(
            lambda x: x.move_id.state == 'posted')
        begining_wip_a_year = sum(begining_wip_aml_A_YEAR.mapped('balance'))
        self.begining_work_in_process_a_year = begining_wip_a_year

        if self.production_amount_a_year > 0:
            self.begining_work_in_process_percent_a_year = self.begining_work_in_process_a_year / \
                self.production_amount_a_year * 100
        else:
            self.begining_work_in_process_percent_a_year = 0
        # ---------------------------------------------------------------------------

        # GET ENDING WORK IN PROCESS WIP
        ending_wip_aml = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
             ('date', '<=', self.date_to)
             ])
        ending_wip_aml = ending_wip_aml.filtered(
            lambda x: x.move_id.state == 'posted')
        self.ending_work_in_process = sum(ending_wip_aml.mapped('balance'))

        if self.production_amount > 0:
            self.ending_work_in_process_percent = self.ending_work_in_process / \
                self.production_amount * 100
        else:
            self.ending_work_in_process_percent = 0.0

        ending_wip_aml_A_YEAR = self.env['account.move.line'].search(
            [('account_id', '=', report_config.persediaan_barang_dalam_proses_account_id.id),
             ('date', '<=', self.date_to)
             ])
        ending_wip_aml_A_YEAR = ending_wip_aml_A_YEAR.filtered(
            lambda x: x.move_id.state == 'posted')
        self.ending_work_in_process_a_year = sum(
            ending_wip_aml_A_YEAR.mapped('balance'))

        if self.production_amount_a_year > 0:
            self.ending_work_in_process_percent_a_year = self.ending_work_in_process_a_year / \
                self.production_amount_a_year * 100
        else:
            self.ending_work_in_process_percent_a_year = 0

        # GET ADJUSTMENT WORK IN PROCESS WIP
        adjs_wip_aml = self.env['account.move.line'].search([
            '&', '&', '&',
            ('account_id', '=',
                 report_config.persediaan_barang_dalam_proses_account_id.id),
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
            ('journal_id', '=', adjustment_journal.id)
        ])
        self.adjustment = sum(adjs_wip_aml.mapped('balance'))

        if self.production_amount > 0:
            self.adjustment_percent = self.adjustment / self.production_amount * 100
        else:
            self.adjustment_percent = 0.0

        adjs_wip_aml_a_year = self.env['account.move.line'].search(
            [
                '&', '&', '&',
                ('account_id', '=',
                 report_config.persediaan_barang_dalam_proses_account_id.id),
                ('date', '>=', first_date_of_this_year),
                ('date', '<=', self.date_to),
                ('journal_id', '=', adjustment_journal.id)
            ])
        self.adjustment_a_year = sum(adjs_wip_aml_a_year.mapped('balance'))

        if self.production_amount_a_year > 0:
            self.adjustment_percent_a_year = self.adjustment_a_year / \
                self.production_amount_a_year * 100
        else:
            self.adjustment_percent_a_year = 0
        # ---------------------------------------------------------------------------

        # get amount of process cost
        proc_cost = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.process_cost_account_id.id),
                ('date_maturity', '>=', self.date_from),
                ('date_maturity', '<=', self.date_to)
             ])

        self.process_cost = sum(proc_cost.mapped(
            'debit')) - sum(proc_cost.mapped('credit'))
        if self.production_amount > 0:
            self.process_cost_percent = self.process_cost / self.production_amount * 100
        else:
            self.process_cost_percent = 0

        proc_cost_a_year = self.env['account.move.line'].search(
            ['&', '&',
                ('account_id', '=', self.process_cost_account_id.id),
                ('date_maturity', '>', year_to_date),
                ('date_maturity', '<=', current_year)
             ])

        self.process_cost_a_year = sum(proc_cost_a_year.mapped(
            'debit')) - sum(proc_cost_a_year.mapped('credit'))
        if self.production_amount_a_year > 0:
            self.process_cost_percent_a_year = self.process_cost_a_year / \
                self.production_amount_a_year * 100
        else:
            self.process_cost_percent_a_year = 0

        # --------------------------------------------------------------

        self.cost_of_material_used_amount = self.begining_material_stock + \
            self.material_net_purchased - self.ending_material_stock - self.material_adjustment
        if self.production_amount > 0:
            self.cost_of_material_used_amount_percent = self.cost_of_material_used_amount / \
                self.production_amount * 100
        else:
            self.cost_of_material_used_amount_percent = 0

        self.cost_of_material_used_amount_a_year = self.begining_material_stock_a_year + \
            self.material_net_purchased_a_year - \
            self.ending_material_stock_a_year - self.material_adjustment_a_year
        if self.production_amount_a_year > 0:
            self.cost_of_material_used_amount_percent_a_year = self.cost_of_material_used_amount_a_year / \
                self.production_amount_a_year * 100
        else:
            self.cost_of_material_used_amount_percent_a_year = 0

        print('get labor cost')
        labor_cost_ids = []
        for acc in gmc_report_config.labor_cost_account_ids:

            # get account move line from this account
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>=', self.date_from),
                 ('date_maturity', '<=', self.date_to)
                 ])
            # get amount from those account move lines
            acc_amount = sum(acc_amls.mapped('debit')) - \
                sum(acc_amls.mapped('credit'))

            if self.production_amount > 0:
                acc_percent = acc_amount / self.production_amount * 100
            else:
                acc_percent = 0

            # get account move line from this account
            acc_amls_a_year = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>', year_to_date),
                 ('date_maturity', '<=', current_year)
                 ])
            # get amount from those account move lines
            acc_amount_a_year = sum(acc_amls_a_year.mapped('debit')) - \
                sum(acc_amls_a_year.mapped('credit'))

            if self.production_amount_a_year > 0:
                acc_percent_a_year = acc_amount_a_year / self.production_amount_a_year * 100
            else:
                acc_percent_a_year = 0

            labor_cost_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount,
                'account_percent': acc_percent,
                'account_value_a_year': acc_amount_a_year,
                'account_percent_a_year': acc_percent_a_year,
            }))

        self.labor_cost.unlink()
        self.labor_cost = labor_cost_ids

        self.labor_cost_amount = sum(self.labor_cost.mapped('account_value'))

        if self.production_amount > 0:
            self.labor_cost_amount_percent = self.labor_cost_amount / self.production_amount * 100
        else:
            self.labor_cost_amount_percent = 0

        self.labor_cost_amount_a_year = sum(
            self.labor_cost.mapped('account_value_a_year'))
        if self.production_amount_a_year > 0:
            self.labor_cost_amount_percent_a_year = self.labor_cost_amount_percent_a_year / \
                self.production_amount_a_year * 100
        else:
            self.labor_cost_amount_percent_a_year = 0

        man_exp_ids = []
        for acc in gmc_report_config.manufacturing_expense_account_ids:
            # get account move line from this account
            acc_amls = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>=', self.date_from),
                 ('date_maturity', '<=', self.date_to)
                 ])
            # get amount from those account move lines
            acc_amount = sum(acc_amls.mapped('debit')) - \
                sum(acc_amls.mapped('credit'))

            if self.production_amount > 0:
                acc_percent = acc_amount / self.production_amount * 100
            else:
                acc_percent = 0

            acc_amls_a_year = self.env['account.move.line'].search(
                ['&', '&',
                 ('account_id', '=', acc.id),
                 ('date_maturity', '>', year_to_date),
                 ('date_maturity', '<=', current_year)
                 ])
            # get amount from those account move lines
            acc_amount_a_year = sum(acc_amls_a_year.mapped('debit')) - \
                sum(acc_amls_a_year.mapped('credit'))

            if self.production_amount_a_year > 0:
                acc_percent_a_year = acc_amount_a_year / self.production_amount_a_year * 100
            else:
                acc_percent_a_year = 0

            man_exp_ids.append((0, 0, {
                'account_id': acc.id,
                'account_value': acc_amount,
                'account_percent': acc_percent,
                'account_value_a_year': acc_amount_a_year,
                'account_percent_a_year': acc_percent_a_year,
            }))

        self.manufacture_expenses.unlink()
        self.manufacture_expenses = man_exp_ids

        self.manufacture_expenses_amount = sum(
            self.manufacture_expenses.mapped('account_value'))
        if self.production_amount > 0:
            self.manufacture_expenses_amount_percent = self.manufacture_expenses_amount / \
                self.production_amount * 100
        else:
            self.manufacture_expenses_amount_percent = 0

        self.manufacture_expenses_amount_a_year = sum(
            self.manufacture_expenses.mapped('account_value_a_year'))
        if self.production_amount_a_year > 0:
            self.manufacture_expenses_amount_percent_a_year = self.manufacture_expenses_amount_a_year / \
                self.production_amount_a_year * 100
        else:
            self.manufacture_expenses_amount_percent_a_year = 0

        # get fiscal year last month and day
        print('Get Fiscal Year Last Month & day')
        # print(self.env.user.company_id.fiscalyear_last_month)
        # print(self.env.user.company_id.fiscalyear_last_day)

        # first_day_a_year_str = str(self.date_from.year) + '-' + str(self.env.user.company_id.fiscalyear_last_month-11) + '-' + '01 00:00:00.243860'
        # first_day_a_year_obj = datetime.strptime(first_day_a_year_str, '%Y-%m-%d %H:%M:%S.%f')

        # last_day_a_year_str = str(self.date_from.year) + '-' + str(self.env.user.company_id.fiscalyear_last_month) + '-' + str(self.env.user.company_id.fiscalyear_last_day) + ' 00:00:00.243860'
        # last_day_a_year_obj = datetime.strptime(last_day_a_year_str, '%Y-%m-%d %H:%M:%S.%f')

        # # print(first_day_a_year_obj.date())
        # print(last_day_a_year_obj.date())

        return self.env.ref('sanwa_manufacturing_cost_report.gross_manufacturing_cost_report_action').report_action(self)
