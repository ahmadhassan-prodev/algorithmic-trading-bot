# helper function to detect correct candlestick pattern
def candlestick_pattern_test(df,c=3):
    last_candle = df.iloc[-c]
    lo = last_candle['Open']
    lc = last_candle['Close']
    lh = last_candle['High']
    ll = last_candle['Low']

    if (lc>lo):
        if ((lc-lo)<=((lh-ll)/6) and lc>=(((lh+ll)/2)+((lh-ll)/4.4)) and lo>((lh+ll)/2)):
            return('Dragonfly doji')

        elif ((lc-lo)<=((lh-ll)/6) and lo<=(((lh+ll)/2)-((lh-ll)/4.4))and lc<((lh+ll)/2)):
            return('Gravestone Doji')

        elif ((lc-lo)<=((lh-ll)/6) and lo>(((lh+ll)/2)-((lh-ll)/4.4)) and lc<(((lh+ll)/2)+((lh-ll)/4.4))):
            return('Simple Doji')
        
        elif((lc-lo)<=((lh-ll)*0.40) and (lc-lo)>((lh-ll)/6) and lc>=(((lh+ll)/2)+((lh-ll)/4)) and lo>(lh+ll)/2):
            return("Right Hammer")

        elif((lc-lo)<=((lh-ll)*0.40) and (lc-lo)>((lh-ll)/6) and lo<=(((lh+ll)/2)-((lh-ll)/4)) and lc<(lh+ll)/2):
            return('Inverted hammer')

        elif((lc-lo)<((lh-ll)/2) and (lc-lo)>((lh-ll)/4) and lo>=(((lh+ll)/2)-((lh-ll)/4)) and lc<=(((lh+ll)/2)+((lh-ll)/4))):
            return('Spinning Top')
        
        else:
            return None

    elif(lc<lo):
        if ((lo-lc)<=((lh-ll)/6) and lo>=(((lh+ll)/2)+((lh-ll)/4.4))and lc>((lh+ll)/2)):
            return('Dragonfly doji')

        elif ((lo-lc)<=((lh-ll)/6) and lc<=(((lh+ll)/2)-((lh-ll)/4.4))and lo<((lh+ll)/2)):
            return('Gravestone Doji')

        elif((lo-lc)<=((lh-ll)/6) and lc>(((lh+ll)/2)-((lh-ll)/4.4)) and lo<(((lh+ll)/2)+((lh-ll)/4.4))):
            return('Simple Doji')
        
        elif((lo-lc)<((lh-ll)*0.40) and (lo-lc)>=((lh-ll)/6) and lc>(lh+ll)/2 and lo>=(((lh+ll)/2)+((lh-ll)/4))):
            return("Right Hammer")

        elif((lc-lo)<=((lh-ll)*0.40) and (lo-lc)>=((lh-ll)/6) and lo<(lh+ll)/2 and lc<=(((lh+ll)/2)-((lh-ll)/4))):
            return('Inverted hammer')
        
        elif((lo-lc)<((lh-ll)/2) and (lo-lc)>((lh-ll)/4) and lc>=(((lh+ll)/2)-((lh-ll)/4)) and lo<=(((lh+ll)/2)+((lh-ll)/4))):
            return('Spinning Top')
        
        else:
            return None

    elif(lc==lo):
        if(lc>=(((lh+ll)/2)+((lh-ll)/4.4))):
            return('Dragonfly doji')

        elif(lc<=(((lh+ll)/2)-((lh-ll)/4.4))):
            return('Gravestone doji')

        else:
            return('Simple Doji')


# detect candle pattern
def detect_candlestick_pattern(df,c=2):
    # Get details about last complete candle
    # c = 2
    last_candle = df.iloc[-c]
    lo = last_candle['Open']
    lc = last_candle['Close']
    lh = last_candle['High']
    ll = last_candle['Low']

    # Second Last candle
    previous_candle = df.iloc[-(c+1)]
    po = previous_candle['Open']
    pc = previous_candle['Close']
    ph = previous_candle['High']
    pl = previous_candle['Low']

    # print(previous_candle)
    print(last_candle)
    pre_candle = candlestick_pattern_test(df)
    # print(f"previous candle: {pre_candle}")

    # detect candlestick pattern if previous candle is in list of following candles
    if(pre_candle == 'Dragonfly doji' or pre_candle == 'Gravestone Doji' or pre_candle == 'Simple Doji' or pre_candle == "Right Hammer" or pre_candle == 'Inverted hammer' or pre_candle == 'Spinning Top'):
        if (lc>lo):
            upper_diff = lh-lc
            lower_diff = lo-ll
            margin_diff = None
            if(upper_diff<lower_diff):
                margin_diff = upper_diff * 2
            elif(lower_diff<upper_diff):
                margin_diff = lower_diff * 2

            if ((lc-lo)<=((lh-ll)/6) and lc>=(((lh+ll)/2)+((lh-ll)/4.4)) and lo>((lh+ll)/2)):
                return('Dragonfly doji')
                # (lc-lo)<=((lh-ll)/4)

            elif ((lc-lo)<=((lh-ll)/6) and lo<=(((lh+ll)/2)-((lh-ll)/4.4))and lc<((lh+ll)/2)):
                return('Gravestone Doji')

            elif ((lc-lo)<=((lh-ll)/6) and lo>(((lh+ll)/2)-((lh-ll)/4.4)) and lc<(((lh+ll)/2)+((lh-ll)/4.4))):
                return('Simple Doji')
            
            elif((lc-lo)<=((lh-ll)*0.40) and (lc-lo)>((lh-ll)/6) and lc>=(((lh+ll)/2)+((lh-ll)/4)) and lo>(lh+ll)/2):
                return("Right Hammer")

            elif((lc-lo)<=((lh-ll)*0.40) and (lc-lo)>((lh-ll)/6) and lo<=(((lh+ll)/2)-((lh-ll)/4)) and lc<(lh+ll)/2):
                return('Inverted hammer')

            elif (pc<po and lc>=po and (lo<=pc or lo>=pc) and (((lc-lo)<((po-pc)*1.5)) or (lc>ph and ((lc-lo)<((ph-pl)*1.25)) and ((lc-lo)<((po-pc)*3)) and ((ph-pl)<(lh-ll)*1.25))) and (((lo-ll)>0.02 and (lh-lc)>0.02 and ((pc-pl)>0.02 or (ph-po)>0.02)) or ((pc-pl)>0.02 and (ph-po)>0.02 and (lh-lc)>0.02) or ((ph-po)>0.02 and (lh-lc)>0.02 and pl==ll and pc==lo))):
                return('Bullish Engulfing')
            
            elif(((((lo-ll)<=(((lh-lc)+((lh-lc)*0.02)))) and ((lo-ll) >= ((lh-lc)-((lh-lc)*0.02))) and ((lh-lc)<=(((lo-ll)+((lo-ll)*0.02)))) and ((lh-lc) >= ((lo-ll)-((lo-ll)*0.02)))) or
                (((lc-lo)>(lh-ll)*0.75) and upper_diff<=margin_diff and lower_diff<=margin_diff and margin_diff<(upper_diff + lower_diff ))) and ll!=lo and lh!=lc):
                return('Reversal')

            elif(pc<po and lc>((pc + (po-pc)*0.60)) and lc<po and (((pc-pl>0.02 or ph-po>0.02) and (lo-ll>0.02 and lh-lc>0.02)) or ((pc-pl>0.02 and ph-po>0.02) and lh-lc>0.02) or ((ph-po)>0.02 and (lh-lc)>0.02 and pl==ll and pc==lo)) and ph!=po and (lh<ph or lh-lc < lo-ll or ll==lo)):
                return('Bullish Marubuzu')
            
            elif((lc-lo)<((lh-ll)/2) and (lc-lo)>((lh-ll)/4) and lo>=(((lh+ll)/2)-((lh-ll)/4)) and lc<=(((lh+ll)/2)+((lh-ll)/4))):
                return('Spinning Top')

            else:
                return None

        elif(lc<lo):
            upper_diff = lh-lo
            lower_diff = lc-ll
            margin_diff = None
            if(upper_diff<lower_diff):
                margin_diff = upper_diff * 2
            elif(lower_diff<upper_diff):
                margin_diff = lower_diff * 2

            if ((lo-lc)<=((lh-ll)/6) and lo>=(((lh+ll)/2)+((lh-ll)/4.4))and lc>((lh+ll)/2)):
                return('Dragonfly doji')

            elif ((lo-lc)<=((lh-ll)/6) and lc<=(((lh+ll)/2)-((lh-ll)/4.4))and lo<((lh+ll)/2)):
                return('Gravestone Doji')

            elif((lo-lc)<=((lh-ll)/6) and lc>(((lh+ll)/2)-((lh-ll)/4.4)) and lo<(((lh+ll)/2)+((lh-ll)/4.4))):
                return('Simple Doji')
            
            elif((lo-lc)<((lh-ll)*0.40) and (lo-lc)>=((lh-ll)/6) and lc>(lh+ll)/2 and lo>=(((lh+ll)/2)+((lh-ll)/4))):
                return("Right Hammer")

            elif((lc-lo)<=((lh-ll)*0.40) and (lo-lc)>=((lh-ll)/6) and lo<(lh+ll)/2 and lc<=(((lh+ll)/2)-((lh-ll)/4))):
                return('Inverted hammer')

            elif (pc>po and lc<=po and (lo<=pc or lo>=pc) and (((lo-lc)<((pc-po)*1.5)) or (lc<pl and ((lo-lc)<((ph-pl)*1.25)) and ((lo-lc)<((pc-po)*3)) and ((ph-pl)<(lh-ll)*1.25))) and (((lc-ll)>0.02 and (lh-lo)>0.02 and ((po-pl)>0.02 or (ph-pc)>0.02)) or ((po-pl)>0.02 and (ph-pc)>0.02 and (lc-ll)>0.02 ) or ((po-pl)>0.02 and (lc-ll)>0.02 and ph==lh and pc==lo))):
                return('Bearish Engulfing')
            
            elif(((((lc-ll)<=(((lh-lo)+((lh-lo)*0.02)))) and ((lc-ll) >= ((lh-lo)-((lh-lo)*0.02))) and ((lh-lo)<=(((lc-ll)+((lc-ll)*0.02)))) and ((lh-lo) >= ((lc-ll)-((lc-ll)*0.02)))) or 
                (((lo-lc)>(lh-ll)*0.75) and upper_diff<=margin_diff and lower_diff<=margin_diff and margin_diff<(upper_diff + lower_diff ))) and ll!=lc and lh!=lo):
                return('Reversal')

            elif(pc>po and lc<((pc - (pc-po)*0.60)) and lc>po and (((ph-pc>0.02 or po-pl>0.02) and (lh-lo>0.02 and lc-ll>0.02)) or ((ph-pc>0.02 and po-pl>0.02) and lc!=ll) or ((po-pl)>0.02 and (lc-ll)>0.02 and ph==lh and pc==lo)) and pl!=po):
                return('Bearish Marubuzu')
            
            elif((lo-lc)<((lh-ll)/2) and (lo-lc)>((lh-ll)/4) and lc>=(((lh+ll)/2)-((lh-ll)/4)) and lo<=(((lh+ll)/2)+((lh-ll)/4))):
                return('Spinning Top')
            
            else:
                return None

        elif(lc==lo):
            if(lc>=(((lh+ll)/2)+((lh-ll)/4.4))):
                return('Dragonfly doji')

            elif(lc<=(((lh+ll)/2)-((lh-ll)/4.4))):
                return('Gravestone doji')

            else:
                return('Simple Doji')
            
    # detect candlestick pattern if previous candle is not in list of specific candles
    else:
        if (lc>lo):
            upper_diff = lh-lc
            lower_diff = lo-ll
            margin_diff = None
            if(upper_diff<lower_diff):
                margin_diff = upper_diff * 2
            elif(lower_diff<upper_diff):
                margin_diff = lower_diff * 2
            
            if (pc<po and lc>=po and (lo<=pc or lo>=pc) and (((lc-lo)<((po-pc)*1.5)) or (lc>ph and ((lc-lo)<((ph-pl)*1.25)) and ((lc-lo)<((po-pc)*3)) and ((ph-pl)<(lh-ll)*1.25))) and (((lo-ll)>0.02 and (lh-lc)>0.02 and ((pc-pl)>0.02 or (ph-po)>0.02)) or ((pc-pl)>0.02 and (ph-po)>0.02 and (lh-lc)>0.02) or ((ph-po)>0.02 and (lh-lc)>0.02 and pl==ll and pc==lo))):
                return('Bullish Engulfing')

            elif(((((lo-ll)<=(((lh-lc)+((lh-lc)*0.02)))) and ((lo-ll) >= ((lh-lc)-((lh-lc)*0.02))) and ((lh-lc)<=(((lo-ll)+((lo-ll)*0.02)))) and ((lh-lc) >= ((lo-ll)-((lo-ll)*0.02)))) or
                (((lc-lo)>(lh-ll)*0.75) and upper_diff<=margin_diff and lower_diff<=margin_diff and margin_diff<(upper_diff + lower_diff ))) and ll!=lo and lh!=lc):
                return('Reversal')

            elif(pc<po and lc>((pc + (po-pc)*0.60)) and lc<po and (((pc-pl>0.02 or ph-po>0.02) and (lo-ll>0.02 and lh-lc>0.02)) or ((pc-pl>0.02 and ph-po>0.02) and lh-lc>0.02) or ((ph-po)>0.02 and (lh-lc)>0.02 and pl==ll and pc==lo)) and ph!=po and (lh<ph or lh-lc < lo-ll or ll==lo)):
                return('Bullish Marubuzu')

            elif ((lc-lo)<=((lh-ll)/6) and lc>=(((lh+ll)/2)+((lh-ll)/4.4)) and lo>((lh+ll)/2)):
                return('Dragonfly doji')

            elif ((lc-lo)<=((lh-ll)/6) and lo<=(((lh+ll)/2)-((lh-ll)/4.4))and lc<((lh+ll)/2)):
                return('Gravestone Doji')

            elif ((lc-lo)<=((lh-ll)/6) and lo>(((lh+ll)/2)-((lh-ll)/4.4)) and lc<(((lh+ll)/2)+((lh-ll)/4.4))):
                return('Simple Doji')
            
            elif((lc-lo)<=((lh-ll)*0.40) and (lc-lo)>((lh-ll)/6) and lc>=(((lh+ll)/2)+((lh-ll)/4)) and lo>(lh+ll)/2):
                return("Right Hammer")

            elif((lc-lo)<=((lh-ll)*0.40) and (lc-lo)>((lh-ll)/6) and lo<=(((lh+ll)/2)-((lh-ll)/4)) and lc<(lh+ll)/2):
                return('Inverted hammer')

            elif((lc-lo)<((lh-ll)/2) and (lc-lo)>((lh-ll)/4) and lo>=(((lh+ll)/2)-((lh-ll)/4)) and lc<=(((lh+ll)/2)+((lh-ll)/4))):
                return('Spinning Top')

            else:
                return None

        elif(lc<lo):
            upper_diff = lh-lo
            lower_diff = lc-ll
            margin_diff = None
            if(upper_diff<lower_diff):
                margin_diff = upper_diff * 2
            elif(lower_diff<upper_diff):
                margin_diff = lower_diff * 2

            if (pc>po and lc<=po and (lo<=pc or lo>=pc) and (((lo-lc)<((pc-po)*1.5)) or (lc<pl and ((lo-lc)<((ph-pl)*1.25)) and ((lo-lc)<((pc-po)*3)) and ((ph-pl)<(lh-ll)*1.25))) and (((lc-ll)>0.02 and (lh-lo)>0.02 and ((po-pl)>0.02 or (ph-pc)>0.02)) or ((po-pl)>0.02 and (ph-pc)>0.02 and (lc-ll)>0.02 ) or ((po-pl)>0.02 and (lc-ll)>0.02 and ph==lh and pc==lo))):
                return('Bearish Engulfing')
            
            elif(((((lc-ll)<=(((lh-lo)+((lh-lo)*0.02)))) and ((lc-ll) >= ((lh-lo)-((lh-lo)*0.02))) and ((lh-lo)<=(((lc-ll)+((lc-ll)*0.02)))) and ((lh-lo) >= ((lc-ll)-((lc-ll)*0.02)))) or 
                (((lo-lc)>(lh-ll)*0.75) and upper_diff<=margin_diff and lower_diff<=margin_diff and margin_diff<(upper_diff + lower_diff ))) and ll!=lc and lh!=lo):
                return('Reversal')

            elif(pc>po and lc<((pc - (pc-po)*0.60)) and lc>po and (((ph-pc>0.02 or po-pl>0.02) and (lh-lo>0.02 and lc-ll>0.02)) or ((ph-pc>0.02 and po-pl>0.02) and lc!=ll) or ((po-pl)>0.02 and (lc-ll)>0.02 and ph==lh and pc==lo)) and pl!=po):
                return('Bearish Marubuzu')

            elif ((lo-lc)<=((lh-ll)/6) and lo>=(((lh+ll)/2)+((lh-ll)/4.4))and lc>((lh+ll)/2)):
                return('Dragonfly doji')

            elif ((lo-lc)<=((lh-ll)/6) and lc<=(((lh+ll)/2)-((lh-ll)/4.4))and lo<((lh+ll)/2)):
                return('Gravestone Doji')

            elif((lo-lc)<=((lh-ll)/6) and lc>(((lh+ll)/2)-((lh-ll)/4.4)) and lo<(((lh+ll)/2)+((lh-ll)/4.4))):
                return('Simple Doji')
            
            elif((lo-lc)<((lh-ll)*0.40) and (lo-lc)>=((lh-ll)/6) and lc>(lh+ll)/2 and lo>=(((lh+ll)/2)+((lh-ll)/4))):
                return("Right Hammer")

            elif((lc-lo)<=((lh-ll)*0.40) and (lo-lc)>=((lh-ll)/6) and lo<(lh+ll)/2 and lc<=(((lh+ll)/2)-((lh-ll)/4))):
                return('Inverted hammer')
            
            elif((lo-lc)<((lh-ll)/2) and (lo-lc)>((lh-ll)/4) and lc>=(((lh+ll)/2)-((lh-ll)/4)) and lo<=(((lh+ll)/2)+((lh-ll)/4))):
                return('Spinning Top')
            
            else:
                return None

        elif(lc==lo):
            if(lc>=(((lh+ll)/2)+((lh-ll)/4.4))):
                return('Dragonfly doji')

            elif(lc<=(((lh+ll)/2)-((lh-ll)/4.4))):
                return('Gravestone doji')

            else:
                return('Simple Doji')
            

# methode to check candle type
def candle_type(df,c=2):
    last_candle = df.iloc[-c]
    lo = last_candle['Open']
    lc = last_candle['Close']
    lh = last_candle['High']
    ll = last_candle['Low']

    if(lc>lo):
        return 'Bullish candle'
    elif(lc<lo):
        return 'Bearish candle'
    else:
        return 'Doji'