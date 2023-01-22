"""
Chaimae ERREBIAI - Matthieu AKHAVAN NIAKI
"""

import tkinter as tkt
from tkinter import messagebox
from tkinter import ttk
from projet_covoi import is_noyau, stand_alone_cost, resolution_du_pbm


App = tkt.Tk()
App.title("Application")
App.minsize(780, 650)
# App.geometry("800x600")
App.resizable(True, True)
h = tkt.Scrollbar(App)
h.pack(side = tkt.RIGHT, fill = tkt.Y)

label_title = tkt.Label(App, text="Partage des coûts de covoiturage", font='Helvetica 18 bold')
label1 = tkt.Label(App, text = "Nombre de personnes ")
label2 = tkt.Label(App, text="Trajet : ")
label3 = tkt.Label(App, text="Ville de départ ")
label4 = tkt.Label(App, text="Destination ")
label5 = tkt.Label(App, text="Voyageurs ")
label6 = tkt.Label(App, text="Coût du km ")

var_cost = tkt.IntVar(value=1)
var_depart = tkt.StringVar(value="Albi")
var_destin = tkt.StringVar(value="Toulouse")
var_nb = tkt.IntVar(value=3)

entry_depart = tkt.Entry(App, textvariable= var_depart)
entry_dest = tkt.Entry(App, textvariable=var_destin)
entry_cost = tkt.Entry(App, width=10, textvariable=var_cost)
spin_ = tkt.Entry(App, width=3, textvariable=var_nb)

#########################################################################

# table des voyageurs
set = ttk.Treeview(App)
set.place(x=120, y=220)

set['columns']= ('nom', 'ville','distance')
set.column("#0", width=0,  stretch=tkt.NO)
set.column("nom",anchor=tkt.CENTER, width=120)
set.column("ville",anchor=tkt.CENTER, width=80)
set.column("distance",anchor=tkt.CENTER, width=80)

set.heading("#0",text="",anchor=tkt.CENTER)
set.heading("nom",text="Nom Voyageur",anchor=tkt.CENTER)
set.heading("ville",text="Ville",anchor=tkt.CENTER)
set.heading("distance",text="Distance",anchor=tkt.CENTER)

global count
count=0

Input_frame = tkt.Frame(App)
Input_frame.place(x=80, y=500 )

name= tkt.Label(Input_frame,text="Nom du voyageur")
name.grid(row=0,column=0)

city = tkt.Label(Input_frame,text="Destination")
city.grid(row=0,column=1)

distance = tkt.Label(Input_frame,text="Distance au départ")
distance.grid(row=0,column=2)

name_entry = tkt.Entry(Input_frame)
name_entry.insert(0,"Sylvain")
name_entry.grid(row=1,column=0)

city_entry = tkt.Entry(Input_frame)
city_entry.insert(0,"Saint-Suplice")
city_entry.grid(row=1,column=1)

distance_entry = tkt.Entry(Input_frame)
distance_entry.insert(0,"48")
distance_entry.grid(row=1,column=2)


def input_record():    
    global count     
    set.insert(parent='',index='end',iid = count,text='',values=(name_entry.get(),city_entry.get(),distance_entry.get()))
    count += 1
    name_entry.delete(0,tkt.END)
    city_entry.delete(0,tkt.END)
    distance_entry.delete(0,tkt.END)
    if count < var_nb.get():
        pre_input_traveler(count)


def pre_input_traveler(nb_traveler):
    name_entry.insert(0,"Voyageur"+str(nb_traveler + 1))
    city_entry.insert(0,var_destin.get())
    distance_entry.insert(0,"77")


#button
Input_button = tkt.Button(App,text = "Ajouter voyageur",command= input_record)
Input_button.place(x=200, y=550 )

# frame to display the result
Output_frame = tkt.Frame(App)
Output_frame.place(x=480, y=180 ) # mm

var1 = tkt.StringVar()


def control():
    nb = var_nb.get()
    cost = var_cost.get()
    dpt = var_depart.get()
    destin = var_destin.get()
    if nb<2 or nb>5:
        messagebox.showerror("Erreur", "Le nombre de personnes doit être entre 2 et 5")
    if nb != count:
        messagebox.showerror("Erreur", "Veuillez ajouter "+str(count)+" voyayeurs")    
    if type(cost) != int:
        messagebox.showerror("Erreur", "Veuillez saisir un coût valide") 
    elif dpt == destin :
        messagebox.showerror("Erreur", "le départ est la destination doivent être differents")
    else:
        decision_fct()


voyageurs = []
Dist = []
taille = var_nb.get()
prixkm = var_cost.get()


def decision_fct():
    var1 = tkt.StringVar()
    global voyageurs, Dist, taille, prixkm
    prixkm = var_cost.get()
    taille = var_nb.get()
    # r = ""
    for item in set.get_children():
        # grab item id
        id = set.index(item)
        # grab item values : info d'un voyageur
        y = set.item(id, 'values')
        
        x = int(y[2]) * prixkm
        print(x, type(x), type (prixkm), prixkm)
        # list of distances
        Dist.append(x)
        # list of passengers
        voyageurs.append((y[0], y[1], x))

    r1, r2, r3, r4, r5, r6, r7 = resolution_du_pbm(taille,prixkm,voyageurs,Dist)
    r = ""
    rr = ""
    for j in r4:
        r = r + j
    for t in r5:
        rr = rr + t
    result = "Le coût total est de : "+str(r1)+"\n"+r2+"\n"+r3+"\n"+r+"\n"+r6+"\n"+r7+"\n"+rr
    res_label = tkt.Label(Output_frame, textvariable=var1)
    var1.set(result)
    res_label.pack()


def delete_fct():
    entry_depart.delete(0, tkt.END)
    entry_dest.delete(0, tkt.END)
    for item in set.get_children():
      set.delete(item)


# new window for allocation test
entry_values = []
new_window = ''
ent1 = ''
ent2 = ''
ent3 = ''
ent4 = ''
ent5 = ''


def allocation_window():
    global new_window, ent1, ent2, ent3, ent4, ent5, entry_values
    new_window = tkt.Toplevel(App)
    new_window.minsize(350, 500)
    new_window.title("Test d'allocation")
    lbl = tkt.Label(new_window, text="Test des allocations")
    lbl.pack()
    btn1 = tkt.Button(new_window, text="initialiser", command=delete2)
    btn2 = tkt.Button(new_window, text="Tester les allocations", command=allocation_test)

    lblc = tkt.Label(new_window, text="Les couts ")
    lblc.pack()

    ent1_var = tkt.StringVar()
    ent1 = tkt.Entry(new_window, textvariable=ent1_var)
    ent1.pack()
    entry_values.append(ent1_var)
    ent21 = tkt.StringVar()
    ent2 = tkt.Entry(new_window, textvariable=ent21)
    ent2.pack()
    entry_values.append(ent21)
    ent31 = tkt.StringVar()
    ent3 = tkt.Entry(new_window, textvariable=ent31)
    ent3.pack()
    entry_values.append(ent31)
    ent41 = tkt.StringVar()
    ent4 = tkt.Entry(new_window, textvariable=ent41)
    ent4.pack()
    entry_values.append(ent41)
    ent51 = tkt.StringVar()
    ent5 = tkt.Entry(new_window, textvariable=ent51)
    ent5.pack()
    entry_values.append(ent51)

    btn2.pack()
    btn1.pack()


def delete2():
    global ent1, ent2, ent3, ent4, ent5
    ent1.delete(0, tkt.END)
    ent2.delete(0, tkt.END)
    ent3.delete(0, tkt.END)
    ent4.delete(0, tkt.END)
    ent5.delete(0, tkt.END)


def allocation_test():
    l = []
    global Dist, voyageurs, taille, entry_values
    print(entry_values)
    for i in range(taille):
        a = entry_values[i].get()
        l.append(int(a))
    
    prop = tkt.Label(new_window, text="Allocations : "+ str(l))
    prop.pack()
    maxi = max(Dist)
    print(maxi, type(maxi) ,Dist[0])
    if sum(l) != maxi:
        print1 = tkt.Label(new_window, text="La somme de cette allocation est différente du coût total.")
        print1.pack()
    print2 = tkt.Label(new_window, text="Voici les mecontents pour le stand alone test : ")
    print2.pack()
    stand_alone = stand_alone_cost(voyageurs, l)
    r_ = ""
    for k in stand_alone:
        r_ = r_ + k + "\n"
    print3 = tkt.Label(new_window, text=""+r_)
    print3.pack()
    print4 = tkt.Label(new_window, text="Voici les binomes mécontents pour le test noyau (vide si allocation noyau): ")
    print4.pack()
    mct2,css2 = is_noyau(voyageurs, l, 2)
    print5 = tkt.Label(new_window, text=str(mct2)+"\nAvec les couts si seuls par binome"+str(css2)+"\n")
    print5.pack()
    if len(voyageurs) >2 :
        print6 = tkt.Label(new_window, text="Voici les trinomes mécontents pour le test noyau (vide si allocation noyau): ")
        print6.pack()
        mct3,css3 = is_noyau(voyageurs, l, 3)
        print7 = tkt.Label(new_window, text=str(mct3)+"\nAvec les couts si seuls par trinome"+str(css3)+"\n")
        print7.pack()


# button to display the results
btn_calcul = tkt.Button(App, text="Calculer ", width=15, background="Green", command=decision_fct)
# btn to emty the entries
btn_init = tkt.Button(App, text="Initialiser", width=15, command=delete_fct)
# btn for the allocation test window
btn_test = tkt.Button(App, text="Test d'allocation", width=15, command=allocation_window)


label_title.place(x=170, y= 50)
label1.place(x=50, y=110)
label2.place(x=50, y=140)
label3.place(x=95, y=140)
label4.place(x=95, y=160)
label5.place(x=50, y=220)
label6.place(x=400, y=110)
spin_.place(x=200, y=110)
entry_depart.place(x=200 , y=140 )
entry_dest.place(x=200 , y=160 )
entry_cost.place(x= 500 , y=110)

btn_calcul.place(x=110, y=590 ) # 200 550
btn_init.place(x=240, y=590)
btn_test.place(x=180, y=620)

App.mainloop()
