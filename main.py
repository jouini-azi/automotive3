import pandas as pd
import ast
def extract():
    #read data
    with open("fichier trace" ,"r+") as input_file:
        trace = input_file.read()
        trace=trace.strip()
        trace=trace.replace("  ", " ")
        input_file.close()
    #write data
    with open("fichier trace","w") as input_file:
        input_file.write(trace)
        input_file.close()
    my_list=[]
    tableau=trace.split(" ")
    for num in tableau:
        if num !='\n':
            my_list.append(num)
    veh_id=[]
    slot_reservé=[]
    veh_source=[]
    instant=[]
    les_cases_réservées=[]
    for i in range(0,len(my_list),104):
        veh_id.append(my_list[i])
        slot_reservé.append(my_list[i+1])
        veh_source.append(my_list[i+2])
        instant.append(my_list[i+3])
        les_cases_réservées.append(my_list[i+4:i+104])
    # dictionary of lists 
    dict = {'veh id': veh_id, 'slot reservé': slot_reservé, 'veh source': veh_source ,'instant':instant,'les cases réservées': les_cases_réservées} 
    df = pd.DataFrame(dict)
    df.to_csv("matrice interne.csv",index=False)
    return df
def manipulate():
    df_2 = pd.read_csv("matrice interne.csv")
    df_2["premières réservations"] =0
    df_2["Nombre de réservation"] = 0
    df_2["diffrence"]=0
    df_2["Réservation non utilisé"]=0
    max=0
    b = df_2.iloc[0,4]
    b = b.strip('"')
    b=ast.literal_eval(b)
    #Nombre de réservation
    veh_id=df_2["veh id"].unique()
    for id in veh_id:
        vehid=df_2[df_2["veh id"]==id]
        nbreservation=len(vehid["slot reservé"].unique())
        for i in range(0,df_2.shape[0]):
            if df_2.iloc[i,0]==id:
                df_2.iloc[i,6]=nbreservation

    a=df_2.iloc[0,4]
    a = a.strip('"')
    res=ast.literal_eval(a)
    premier_groupe=res[0:33]
    deuxieme_groupe=res[33:76]
    troisiem_groupe=res[77:99]
    premier=premier_groupe.index("-1")
    deuxieme=deuxieme_groupe.index("-1")
    troisiem=troisiem_groupe.index("-1")
    instant=df_2["instant"].unique()
    for i in range(0,df_2.shape[0]):
        a=df_2.iloc[i,4]
        a = a.strip('"')
        res=ast.literal_eval(a)
        premier_groupe=res[0:33]
        deuxieme_groupe=res[33:76]
        troisiem_groupe=res[77:99]
        #premier reservation
        for j in range(premier_groupe.index("-1")):
            if(premier_groupe[j]==str(df_2.iloc[i,2])):
                df_2.iloc[i,5]+=1
            else:
                break
        for j in range(deuxieme_groupe.index("-1")):
            if(deuxieme_groupe[j]==str(df_2.iloc[i,2])):
                df_2.iloc[i,5]+=1
            else:
                break                
        for j in range(troisiem_groupe.index("-1")):
            if(troisiem_groupe[j]==str(df_2.iloc[i,2])):
                df_2.iloc[i,5]+=1
            else:
                break
        while ((premier!=premier_groupe.index("-1")) and(premier<premier_groupe.index("-1")) and(str(premier_groupe[premier])==str(df_2.iloc[i,2]))):
            df_2.iloc[i,5]+=1
            premier=premier_groupe.index("-1")
        while ((deuxieme!=deuxieme_groupe.index("-1")) and (deuxieme<deuxieme_groupe.index("-1")) and (str(deuxieme_groupe[deuxieme])==str(df_2.iloc[i,2]))):
            df_2.iloc[i,5]+=1
            deuxieme=deuxieme_groupe.index("-1")
        while (troisiem!=troisiem_groupe.index("-1") and(troisiem<troisiem_groupe.index("-1")) and ((str(troisiem_groupe[troisiem])==str(df_2.iloc[i,2])))):
            df_2.iloc[i,5]+=1
            troisiem=troisiem_groupe.index("-1")
    #Nombre des slots réservés non utilisés
    for id in veh_id:
        max=0
        mins=1    
        for inst in instant:
            df=df_2.loc[(df_2["instant"]==inst)&(df_2["veh id"]==id)]
            max_inst=df["Nombre de réservation"].max()
            mi=df["Nombre de réservation"].min()
            if max_inst>max:
                max=max_inst  
            if mi<mins:
                mins=mi  
        df_2.loc[df_2["veh id"]==id,"Nombre des slots réservés non utilisés"]=max_inst-mins
        df_2.sort_values(["veh source","instant"],inplace=True)
    return df_2
def output():
    extract()
    dataframe=manipulate()
    Veh_Id =[]
    Nombre_des_reservations=[]
    Nombre_des_premières=[]
    Nombre_dannulation=[]
    Nombre_des_slots_réservés_non_utilisés=[]
    vehsource = dataframe["veh id"].unique()
    for veh_source in vehsource:
        df=dataframe[dataframe["veh id"]==veh_source]
        Veh_Id.append(veh_source)
        Nombre_des_reservations.append(df["Nombre de réservation"].max())
        df_copy = dataframe[dataframe["veh source"]==veh_source]
        Nombre_des_premières.append(df_copy["premières réservations"].max())
        Nombre_des_slots_réservés_non_utilisés.append(int(df["Nombre des slots réservés non utilisés"].sum()/df["Nombre des slots réservés non utilisés"].shape[0]))
    #Dictionary
    data={
        "Veh Id":Veh_Id,
        "Nombre des reservations":Nombre_des_reservations,
        "Nombre des premières réservations":Nombre_des_premières,
        "Nombre d’annulation":0,
        "Nombre des slots réservés non utilisés":Nombre_des_slots_réservés_non_utilisés
    }
    #diffrence
    annsource=[]
    diffsource=[]
    vehsource = dataframe["veh source"].unique()
    vehid = dataframe["veh id"].unique()
    print(vehid)
    for vin in vehid:
        dp= dataframe[dataframe["veh id"]==vin]
        inst = dp["instant"].unique()
        for ins in inst:
            dp_inst = dp.loc[dp["instant"]==ins]
            difference = dp_inst.iloc[0,4]
            for i in range(dp_inst.shape[0]):
                if(dp_inst.iloc[i,4]!=difference):
                    annsource.append(dp_inst.iloc[i,2])
        for v in vehsource:
            diff=0
            for i in annsource:
                if(str(v)==str(i)):
                    diff+=1
        diffsource.append(diff)
    #Dataframe
    dataframe.to_csv("matrice output.csv",index=False)
    dataframe = pd.DataFrame(data)
    dataframe["Nombre d’annulation"]=diffsource
    dataframe.to_csv("output.csv",index=False)
output()       
