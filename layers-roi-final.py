
"""
Created on Thu Oct 26 12:23:54 2023
@author: guilherme borchardt
Estimation of layer performance using a probiotc as a feed additive.

Version: 1+

add local currency based on system default

"""

import PySimpleGUI as psg
import numpy as np
import babel.numbers
from decimal import Decimal
#import decimal
#import babel
from babel import numbers
#import babel
import locale
   

def main():
    app_title='ROI Estimation - Commercial Layers'
    app_version='v. 1.0+ working'
    
 
    # setup enviroment
    
    np.random.seed(1234)
    egg_price_units = 12 # price for each unit
    numbers_of_std_desv = 1.96 # to be used in std desv on normal distrib.
    distrib = 'u'# info that determine the type of distribution will be generated. Accepts:  U for uniform / N for normal
    
    # for theme refer to pysimpleGUI modul
    psg.theme('SystemDefault')
    psg.set_options(font='calibri 14', button_element_size=(1,1))
    
    # input fields config
    input_field_size=(17,1)
    input_size_lbl=(20,1)
    
    # slider config
    slider_prim_size=(20,15)
    slider_secund_size = (15,10)
    '''
    button_menu_def = [
        ['Currency', 'Production']
         ]
    '''
    # define currency  -- World currency symbols list - names, country, codes and symbols
    currency_menu= ['EUR','BRL', 'ZAR', 'DKK', 'USD', 'EGP', 'LBP', 'NAD', 'PKR', 'PLN', 'SAR', 'GBP', 'SEK', 'CHF', 'THB', 'TRY']
    currency_default=currency_menu[4] # default USD
    currency_menu.sort()
    # define footnotes      
    rodape_text = f'Code Version: {app_version}, -- Guilherme Borchardt, 2023 --'
    
    layout = [
        
        [psg.Text('Parameter:', size=input_size_lbl, justification='center'),
         psg.Text('Average', size=input_size_lbl, justification='center'),
         psg.Text('Variation (%)', justification='left')],
        [psg.Text('Egg Price (retail / dozen):', size=input_size_lbl, justification='left'),
         psg.Input('20', key='-EGG_PRICE_AVER-', size=input_field_size, justification='center'),
         psg.Slider(range=(1,20), size=slider_secund_size, expand_x=False, default_value=10, enable_events=True ,orientation='h', key='-SL_EGG_PRICE-')],
        [psg.Text('Feed Cost (ton):', size=input_size_lbl, justification='left'),
         psg.Input('2000', key='-FEED_PRICE_AVER-', size=input_field_size, justification='center'),
         psg.Slider(range=(1,20), size=slider_secund_size,expand_x=False, default_value=10, enable_events=True ,orientation='h', key='-SL_FEED_PRICE-')],
        
        [psg.Text('Daily feed intake / hen(g):', size=input_size_lbl, justification='left'),
         psg.Input('100', key='-FEED_INTAKE_AVER-', size=input_field_size, justification='center'),
         psg.Text('Hen housed eggs / cycle', size=input_size_lbl, justification='center')],
        [psg.Text('Age (weeks):', size=input_size_lbl, justification='left'),
         psg.Input('100', key='-PROD_WEEKS-', size=input_field_size, justification='center'),
         psg.Slider(range=(320,520), size=slider_secund_size, expand_x=False, default_value=420, enable_events=True ,orientation='h', key='-SL_TOTAL_EGG_CYCLE-')],
        [psg.Text('Probiotic Cost / Mton:', size=input_size_lbl, justification='left'), psg.Input('50', key='-PROB_COST-', size=input_field_size, justification='center')],
        [psg.Text('Increase on Laying rate (%)', size=input_size_lbl, justification='center', expand_x=True),
         psg.Text('Redution on Mortality rate (%)', size=input_size_lbl, justification='center', expand_x=True)],
        [psg.Slider(range=(.1,3), size=slider_prim_size, expand_x=True, default_value=1.5, enable_events=True ,orientation='h', key='-SL_LAY_IMPROV-', resolution=.1),
         psg.Slider(range=(0,2), size=slider_prim_size, expand_x=True, default_value=1, enable_events=True ,orientation='h', key='-SL_DELTA_MORT_HEN-', resolution=.1)],
        [psg.Text('NUMBER OF HENS', size=(20,1), justification='center', expand_x=True)],
        [psg.Slider(range=[1,100000], size=slider_prim_size, expand_x=True, default_value=1, enable_events=True ,orientation='h', key='-NUMBER_LAYERS-', resolution=10000)],
       
        [psg.Text('Parameter:     ', size=input_size_lbl, justification='left'),
         psg.Text('Value', size=input_size_lbl, justification='center'),
         psg.Text('', size=input_size_lbl, justification='center')],
        [psg.Text('Delta Hen house eggs:', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-N_EGG_IMPROV-', size=input_field_size, justification='center')],
        [psg.Text('Delta Egg due Mort:', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-N_EGG_DUE_MORT-', size=input_field_size, justification='center')],
        
        [psg.Text('Delta Income:', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-EGG_INCOME_HEN-', size=input_field_size, justification='center')],
        [psg.Text('Probiotic Inv.:', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-PROBIOTIC_COST_HEN-', size=input_field_size, justification='center')],
        [psg.Text('Profit - Probiotic:', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-PROFIT_HEN_PROB-', size=input_field_size, justification='center')], 
        [psg.Text('Profit - Control:', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-PROFIT_HEN_CONTROL-', size=input_field_size, justification='center')],
    
        [psg.Text('Delta Profit(%):', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-DELTA_PROFIT_HEN-', size=input_field_size, justification='center')],
        [psg.Text('ROI (%):', size=input_size_lbl, justification='left'),
         psg.Input('', disabled=True,  key='-ROI-', size=input_field_size, justification='center', font=16)],
        [psg.Text('EVENT LIKELIHOOD (%):', size=input_size_lbl, justification='center', expand_x=True)],
        
        [psg.Slider(range=(99,1),size=slider_prim_size, expand_x=True, default_value=50, enable_events=True ,orientation='h', key='-SL_EVENT_LIKEL-', resolution=1)],
         
        [ psg.Button('Exit', expand_x=False, key='-EXIT-' ),
         psg.Text('Currency:', size=input_size_lbl, justification='right'),
         psg.OptionMenu(currency_menu, key='-CURRENCY-', size=(4,1))],
        [psg.Text(rodape_text, size=input_size_lbl, justification='center', font=("arial 10"), key='-RODAPE-', expand_x=True)],
        
        ]
    
    
    # for currency determination
    def callback(var, index, mode):
        """
        For OptionMenu
        var - tkinter control variable.
        index - index of var, '' if var is not a list.
        mode - 'w' for 'write' here.
        """
        window.write_event_value("-CURRENCY-", window['-CURRENCY-'].TKStringVar.get())
    
    
    def format_currency(value, curr):
    
        #curr_str_atul = babel.numbers.format_currency(decimal.Decimal(value ), curr )
        curr_str_atul = numbers.format_currency(Decimal(value ), curr )
        return curr_str_atul
        '''
        if curr in currency_dict:
            ulocale= (currency_dict[curr])
            curr_str_atul = babel.numbers.format_currency( decimal.Decimal(value ), curr )
            #curr_str_atul = babel.numbers.format_currency(value, curr, locale=ulocale, group_separator=True)
            print(f'I am in function: {curr}')
            return curr_str_atul
        else:
            psg.popup_error(f'ERROR - Currency from {curr} not found! ', keep_on_top=True)
            curr_str_atul = babel.numbers.format_currency(value, 'US', locale='en_US')
            
            return curr_str_atul
        '''
           
        
    def str_to_num_convert(string):
        
        try:
            num = float(string)
            return num
        except ValueError:
            psg.popup_error('ERROR - Please Input a valid NUMBER!\nCODE EXECUTION STOPED', keep_on_top=True)
            return '1'
            
                
    def creat_distrib(aver, perc, distr_type):
        # distrib type - define if it is normal, uniform, triangular
        n=20000 # number of repetitions used in distributions
        if distr_type.upper()=='N': # normal distribution
                std = aver*perc*numbers_of_std_desv
                distrib=np.random.normal(aver,std,n)
                return distrib
        
        if distr_type.upper()=='U': # uniform distribution
                low = aver-(aver*perc)
                high = aver+(aver*perc)
                distrib=np.random.uniform(low,high,n)
                return distrib
       
    def calc_mort_hen_on_tot_egg (egg_tot, tot_mort_perc, wk_mort_perc):
        '''
        According performance manual of Hyline brown
        median of mortality is at 70% of the life cicle (73 weeks for 100 wks cicle)
        the production of a hen reach 72% of the total predicted
         '''
        
        diff_egg = egg_tot * (1-tot_mort_perc/100) + (tot_mort_perc/100 * egg_tot * wk_mort_perc/100)
        tot_delta = egg_tot - diff_egg
        total_egg = egg_tot+tot_delta
        return total_egg    
    
    
    def input_error_verify(str, msn):
        print(type(str))
        if str.isdigit():
            try:
                var = float(str)
                if var <= 0:
                    psg.popup_error(f'Invalid Value of {msn}!', auto_close=True, keep_on_top=True)
                    return True # with input error
        
                return False # with input error
            except:
                psg.popup_error(f'ERROR Value of {msn} - Verify your input', auto_close=True, keep_on_top=True)
                return True # with input error
        
        psg.popup_error(f'Invalid Value of {msn}!\n Only Integer Numbers is accepted !', auto_close=True, keep_on_top=True)
        return True
            
        
    window = psg.Window(f'{app_title} - {app_version}', layout, finalize=True)
    window['-CURRENCY-'].TKStringVar.trace("w", callback)
    
    
    while True:
            
            event, values = window.read()
            
            if event in (psg.WIN_CLOSED, '-EXIT-'):
                break
            
            '''
            if event == '-EGG_PRICE_AVER-':
                new_egg_price = values['-EGG_PRICE_AVER-']
                window['-EGG_PRICE_AVER-'].update(new_egg_price)
                
            if event == '-FEED_PRICE_AVER-':           
                new_feed_price = values['-FEED_PRICE_AVER-']
                window['-FEED_PRICE_AVER-'].update(new_feed_price)
              
            if event == '-FEED_INTAKE_AVER-':           
                new_feed_intake = values['-FEED_INTAKE_AVER-']
                window['-FEED_INTAKE_AVER-'].update(new_feed_intake)   
            
            if event == '-PROD_WEEKS-':           
                new_prod_weeks = values['-PROD_WEEKS-']
                window['-PROD_WEEKS-'].update(new_prod_weeks) 
     
            if event == '-PROB_COST-':
                new_prob_cost = values['-PROB_COST-']
                window['-PROB_COST-'].update(new_prob_cost)
            '''
            
            
            if values['-NUMBER_LAYERS-']==0 or values['-NUMBER_LAYERS-']==None:
                window['-NUMBER_LAYERS-'].update(1)
            
            # verify if user input is correct 
            if input_error_verify(values['-EGG_PRICE_AVER-'], ' EGG PRICE '): 
                window['-EGG_PRICE_AVER-'].update('1')
            
            if input_error_verify(values['-FEED_PRICE_AVER-'], ' FEED COST '): 
                window['-FEED_PRICE_AVER-'].update('1')
            
            if input_error_verify(values['-FEED_INTAKE_AVER-'] , ' FEED INTAKE '): 
                window['-FEED_INTAKE_AVER-'].update('100')
            
            if input_error_verify(values['-PROD_WEEKS-'] , ' PROD_WEEKS '): 
                window['-PROD_WEEKS-'].update('100')
            
            if input_error_verify(values['-PROB_COST-'] , ' PROBIOTIC COST '): 
                window['-PROB_COST-'].update('1')
            
            
            # calculations
            egg_price_aver_num = str_to_num_convert(values['-EGG_PRICE_AVER-'])
            egg_price_var_perc_num = str_to_num_convert(values['-SL_EGG_PRICE-']/100)
            egg_price_distr = creat_distrib(egg_price_aver_num, egg_price_var_perc_num, distrib)/egg_price_units # price por egg
            
            
            feed_price_aver_num = str_to_num_convert(values['-FEED_PRICE_AVER-'])
            feed_price_var_perc_num = str_to_num_convert(values['-SL_FEED_PRICE-']/100)
            feed_price_distr = creat_distrib(feed_price_aver_num, feed_price_var_perc_num, distrib ) 
            
            feed_intake_aver_num = str_to_num_convert(values['-FEED_INTAKE_AVER-'])
            
            prob_cost_aver_num = str_to_num_convert(values['-PROB_COST-'])
            
            prod_weeks_num = str_to_num_convert(values['-PROD_WEEKS-'])
           
            total_eggs_num = str_to_num_convert(values['-SL_TOTAL_EGG_CYCLE-'])
            
            laying_perc_improv_num = str_to_num_convert(values['-SL_LAY_IMPROV-']) 
            
           
            percentil_slider_num = 100-str_to_num_convert(values['-SL_EVENT_LIKEL-'])
            
            # impact of mortality rate on total egg produced
            '''
            According performance manual of Hyline brown
            median of mortality is at 70% of the life cicle (73 weeks for 100 wks cicle)
            the production of a hen reach 72% of the total predicted
            
            '''
            perc_prod_when_mort = 72
            delta_mort_hen_improv = str_to_num_convert(values['-SL_DELTA_MORT_HEN-']) 
            
            tot_egg_consid_delta_mort = calc_mort_hen_on_tot_egg(total_eggs_num, delta_mort_hen_improv, perc_prod_when_mort)
            delta_egg_due_mort=tot_egg_consid_delta_mort-total_eggs_num
            
            # calculations
            
            extra_eggs_hen = total_eggs_num*laying_perc_improv_num/100    
            extra_income_hen = np.percentile((extra_eggs_hen + delta_egg_due_mort) * egg_price_distr, percentil_slider_num)
           
            total_feed_hen = prod_weeks_num * 7 * feed_intake_aver_num / 1000 # correct
            probiotic_cost_hen = prob_cost_aver_num * total_feed_hen  / 1000
            
            total_feed_cost_hen = np.percentile(total_feed_hen * feed_price_distr/1000, percentil_slider_num) # correct
            profit_hen = round(extra_income_hen - probiotic_cost_hen,2)
            
            
            # profit / hen
            
            total_income_egg_hen_control= np.percentile(egg_price_distr * total_eggs_num,percentil_slider_num)# correct
            
            
            profit_hen_control = round(total_income_egg_hen_control - total_feed_cost_hen,2)
            perc_profit_hen = round(profit_hen/profit_hen_control*100,2)
            
            profit_hen_probiotic = round(total_income_egg_hen_control + extra_income_hen - probiotic_cost_hen - total_feed_cost_hen,2)
            perc_profit_hen = round(profit_hen/profit_hen_control*100,2)
            roi=round(profit_hen/probiotic_cost_hen*100,2)
            
            n_layers = str_to_num_convert(values['-NUMBER_LAYERS-'])
            
            if n_layers==0:
                n_layers=1
                window['-NUMBER_LAYERS-'].update(n_layers)
            
            
            currency_choice_str = (values['-CURRENCY-'])
    
            # currency change 
            if  values['-CURRENCY-'] != '':
               
                extra_income_hen_formated = format_currency(extra_income_hen  * n_layers, currency_choice_str)
                prob_cost_total_formated = format_currency(probiotic_cost_hen  * n_layers,  currency_choice_str)
                profit_total_control_formated = format_currency(profit_hen_control * n_layers, currency_choice_str)
                profit_total_probiotic_formated = format_currency(profit_hen_probiotic * n_layers, currency_choice_str)
                #perc_profit_hen_formated = format_currency(perc_profit_hen, currency_choice_str)
              
            else:
                currency_choice_str = currency_default
                extra_income_hen_formated = format_currency(extra_income_hen  * n_layers, currency_choice_str)
                prob_cost_total_formated = format_currency(probiotic_cost_hen  * n_layers,  currency_choice_str)
                profit_total_control_formated = format_currency(profit_hen_control * n_layers, currency_choice_str)
                profit_total_probiotic_formated = format_currency(profit_hen_probiotic * n_layers, currency_choice_str)
                #perc_profit_hen_formated = format_currency(perc_profit_hen, currency_choice_str)
            
            n_decimal=2
            if n_layers!=1:
                n_decimal=0
                
            
            window['-N_EGG_IMPROV-'].update(round(extra_eggs_hen * n_layers,n_decimal))
            window['-N_EGG_DUE_MORT-'].update(round(delta_egg_due_mort * n_layers,n_decimal))
            window['-EGG_INCOME_HEN-'].update(extra_income_hen_formated)
            window['-PROBIOTIC_COST_HEN-'].update(prob_cost_total_formated)
            window['-PROFIT_HEN_CONTROL-'].update(profit_total_control_formated)
            window['-PROFIT_HEN_PROB-'].update(profit_total_probiotic_formated)
            window['-DELTA_PROFIT_HEN-'].update(str(f'{perc_profit_hen} %'))
       
            roi_str = str(f'{roi} %') # ROI with %
            if roi<=0:
                window['-ROI-'].update(roi_str,text_color='#ff0000')
            elif roi>0 and roi<=20:
                window['-ROI-'].update(roi_str, text_color='#ff8916')   
            elif roi>20:
                window['-ROI-'].update(roi_str, text_color='#343ec5')    
            
            
            
            
            
    window.close()



if __name__ == "__main__":
    main()
    
    