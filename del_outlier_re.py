#***type編號***
type=[3,5,10,15,21,23,28,33]

#***設定自變數***
for XX in range(0,8):
    #***設定應變數***
    for YY in range(1,7):    
        
        #***讀入SPSS檔案***
        filepath = r"D:\data_MS\硬體\sav\py_硬體transpose_KU_tech.sav" #檔案不可以同時開著
        df,meta = pyreadstat.read_sav(filepath)
        #***讀入stata檔案***
        #df=pd.read_stata(filepath)

        #***如果有缺值，則使用這行過濾***
        #df.loc[ df.Year != *** ]
        #print(df.head())
   
        #***刪掉幾個observations***
        count = 0
        
        #***第幾個應變數_第幾種種類***
        print("*@@@@@ B"+str(YY)+"_type"+str(type[XX])+" @@@@@")         
        
       
        #***回歸分析***
        while True:
            
            #***自變數 8種***
            #type3 strategicfit_edited
            if XX ==0:
                X = df[['strategicfit_edited','LN_KU1','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]
            #type5 專利數平均+1
            elif XX ==1:
                X = df[['In專利數平均1','LN_KU1','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]
            #type10 competition_past3y1
            elif XX ==2:
                X = df[['Incompetition_past3y1','LN_KU1','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]
            #type15 competition1
            elif XX ==3:
                X = df[['Incompetition1','LN_KU1','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]
            #type21 strategicfit_edited
            elif XX ==4:
                X = df[['strategicfit_edited','LN_KU2','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]
            #type23 專利數平均+1
            elif XX ==5:
                X = df[['In專利數平均1','LN_KU2','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]
            #type28 competition_past3y1
            elif XX ==6:
                X = df[['Incompetition_past3y1','LN_KU2','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]
            #type33 competition1
            else:
                X = df[['Incompetition1','LN_KU2','Ln_Firm_age','Ln_firm_sizeemp','RD_intensityxrdsale','Lnnumberofalliances','LnPatentstock','Technologydiversity_樣本公司_edited','dummy_3571','dummy_3572','dummy_3575','dummy_3577']]


            #***設定應變數B1~B6***
            if YY==1:
                y = df['forwardcitationranking_prior5yearsfixedeffectadjusttop5'].values
            elif YY==2:
                y = df['forwardcitationranking_prior5yearsfixedeffectadjusttop3'].values
            elif YY==3:
                y = df['forwardcitationranking_prior5yearsfixedeffectadjusttop1'].values
            elif YY==4:
                y = df['forwardcitationrankingfixedeffectadjusttop5'].values
            elif YY==5:
                y = df['forwardcitationrankingfixedeffectadjusttop3'].values
            else:
                y = df['forwardcitationrankingfixedeffectadjusttop1'].values            

            
            
            X2 = sm.add_constant(X) 
            res = sm.OLS(y, X2) 
            res = res.fit() 
            beta = res.params
            #print(res.summary()) #總回歸分析與檢驗
            #print(res.params) #beta值
            sum_beta = 0
            for i in range(len(beta)):
                sum_beta = sum_beta+beta[i]
            if sum_beta==0:
                print("all beta = 0") #beta = 0，不能做回歸
                break

            y_array = y.ravel()
            #***求標準殘差之計算***
            #估計值
            predict = res.predict() 
            predict_array = np.array(predict)
            #殘差
            subtract = y_array-predict_array
            #標準化估計 ((Σ(y-y')^2)/n)^1/2
            std_predict = sqrt(sum(np.square(subtract))/len(y_array)) #殘差
            #標準殘差 = 殘差/標準化估計值
            std_subtract = subtract/std_predict
            #print(std_subtract)

            #***取最大的標準殘差位置***
            std_subtract_list = std_subtract.tolist()
            max_std_index = std_subtract_list.index(max(std_subtract_list))
            #print(max(std_subtract_list))
            #print(max_std_index) #比對excel要+2，SPSS則+1

            #***確認是否有標準殘差>3***
            x=0
            #如果有，則 x>0
            for i in range(len(std_subtract)):
                if std_subtract[i]>3.5:
                     x=x+1

            #***刪除那一列***
            if x>0:
                df = pd.DataFrame(df)
                df = df.drop([max_std_index],axis=0)
                df= df.reset_index(drop=True)
                count=count+1
            else:
                break

        #count為刪除多少個observation
        print("count = ",count)

        #***儲存excel檔案**
        #df.to_excel(r"C:\Users\葉之晴\Pictures\11.xlsx",header=True)
        #***儲存SPSS檔案**
        #pyreadstat.write_sav(df, r'D:\data_MS\SPSS整理檔\SPSS_hardware_0414\B1_test111.sav')
        #***儲存stata檔案**
        #檔案路徑設定 D:\data_MS\B(kk)_type(x).dta

        output_path = str(u'D:\data_MS\半導體\dta\暫時資料夾_樣本公司\B'+str(YY)+'_type'+str(type[XX])+'.dta')
        print(output_path)
        df.to_stata(output_path)

    
print("Done!!!")
    