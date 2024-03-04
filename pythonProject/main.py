import tkinter as tk
from tkinter import ttk, messagebox
from Fonction_Algorithme_Optimisation import *
from Fonction_Modification_Graphe import *

class InterfaceGraphique:
    def __init__(self, master, graphe):
        self.master = master
        master.title("Planificateur de voyage")
        self.graphe = graphe

        # Combobox pour la position du voyageur
        self.label_position = tk.Label(master,
                                       text="Position du voyageur:",
                                       anchor="w")
        self.label_position.pack(anchor="w",
                                 padx=40)
        self.position_var = tk.StringVar()
        self.combobox_position = ttk.Combobox(master,
                                              textvariable=self.position_var,
                                              values=les_sommet_de(graphe))
        self.combobox_position.pack(anchor="w",
                                    padx=40)

        # Liste des villes avec des cases à cocher
        self.label_villes = tk.Label(master,
                                     text="Choisir les villes à visiter:",
                                     anchor="w")
        self.label_villes.pack(anchor="w",
                               padx=40)
        self.villes = les_sommet_de(self.graphe)
        self.checkbox_villes = []
        for ville in self.villes:
            var = tk.IntVar()
            checkbox = tk.Checkbutton(master,
                                      text=ville,
                                      variable=var,
                                      anchor="w")
            checkbox.ville = ville  # pour sauvegarder la ville associée à la checkbox
            checkbox.pack(anchor="w",
                          padx=40)
            self.checkbox_villes.append((ville, var))

        # Liste des choix (Optimiser le temps, le coût, les deux)
        self.label_choix = tk.Label(master,
                                    text="Choisir le critère d'optimisation:",
                                    anchor="w")
        self.label_choix.pack(anchor="w",
                              padx=40)
        self.choix_var = tk.IntVar()
        self.radio_temps = tk.Radiobutton(master,
                                          text="Optimiser le temps",
                                          variable=self.choix_var,
                                          value=1,
                                          anchor="w")
        self.radio_temps.pack(anchor="w",
                              padx=40)
        self.radio_cout = tk.Radiobutton(master,
                                         text="Optimiser le coût",
                                         variable=self.choix_var,
                                         value=2,
                                         anchor="w")
        self.radio_cout.pack(anchor="w",
                             padx=40)
        self.radio_temps_cout = tk.Radiobutton(master,
                                               text="Optimiser les deux",
                                               variable=self.choix_var,
                                               value=3,
                                               anchor="w")
        self.radio_temps_cout.pack(anchor="w",
                                   padx=40)

        # Choix entre Aller simple et Aller et retour
        self.label_aller_retour = tk.Label(master,
                                           text="Choisir le type de voyage:",
                                           anchor="w")
        self.label_aller_retour.pack(anchor="w",
                                     padx=40)
        self.choix_aller_retour_var = tk.StringVar()
        self.radio_aller_simple = tk.Radiobutton(master,
                                                 text="Aller simple",
                                                 variable=self.choix_aller_retour_var,
                                                 value="aller_simple",
                                                 anchor="w")
        self.radio_aller_simple.pack(anchor="w",
                                     padx=40)
        self.radio_aller_retour = tk.Radiobutton(master,
                                                 text="Aller et retour",
                                                 variable=self.choix_aller_retour_var,
                                                 value="aller_retour",
                                                 anchor="w")
        self.radio_aller_retour.pack(anchor="w",
                                     padx=40)

        # Bouton Evaluer
        self.button_evaluer = tk.Button(master,
                                        text="Evaluer",
                                        command=self.evaluer)
        self.button_evaluer.pack(anchor="w",
                                 padx=40,
                                 pady=20)

    def evaluer(self):
        position_voyageur = self.position_var.get()
        villes_a_visiter = [position_voyageur] + [ville for ville, var in self.checkbox_villes if var.get() == 1]
        choix_optimisation = self.choix_var.get()
        choix_aller_retour = self.choix_aller_retour_var.get()

        if not position_voyageur or not villes_a_visiter:
            messagebox.showerror("Erreur", "Veuillez sélectionner une position et au moins une ville à visiter.")
            return

        if choix_optimisation not in [1, 2, 3]:
            messagebox.showerror("Erreur", "Choix d'optimisation invalide")
            return

        if choix_aller_retour == "aller_simple":
            if choix_optimisation == 1:
                chemin = optimiser_le_parcours(poids_temps(self.graphe), villes_a_visiter)
                temps = temps_sur_un_chemin(chemin, poids_temps(self.graphe))
                couts = couts_sur_un_chemin(chemin, poids_couts(self.graphe))
                messagebox.showinfo("Résultat", f"Chemin optimal : {chemin}\nTemps : {temps} h\nCoûts : {couts} UM")
            elif choix_optimisation == 2:
                chemin = optimiser_le_parcours(poids_couts(self.graphe), villes_a_visiter)
                temps = temps_sur_un_chemin(chemin, poids_temps(self.graphe))
                couts = couts_sur_un_chemin(chemin, poids_couts(self.graphe))
                messagebox.showinfo("Résultat", f"Chemin optimal : {chemin}\nTemps : {temps} h\nCoûts : {couts} UM")
            elif choix_optimisation == 3:
                chemin = optimiser_le_parcours(poids_temps_couts(self.graphe), villes_a_visiter)
                temps = temps_sur_un_chemin(chemin, poids_temps(self.graphe))
                couts = couts_sur_un_chemin(chemin, poids_couts(self.graphe))
                messagebox.showinfo("Résultat", f"Chemin optimal : {chemin}\nTemps : {temps} h\nCoûts : {couts} UM")
        elif choix_aller_retour == "aller_retour":
            if choix_optimisation == 1:
                chemin = optimiser_le_parcours_aller_retour(poids_temps(self.graphe), villes_a_visiter)
                temps = temps_sur_un_chemin(chemin, poids_temps(self.graphe))
                couts = couts_sur_un_chemin(chemin, poids_couts(self.graphe))
                messagebox.showinfo("Résultat", f"Chemin optimal : {chemin}\nTemps : {temps} h\nCoûts : {couts} UM")
            elif choix_optimisation == 2:
                chemin = optimiser_le_parcours_aller_retour(poids_couts(self.graphe), villes_a_visiter)
                temps = temps_sur_un_chemin(chemin, poids_temps(self.graphe))
                couts = couts_sur_un_chemin(chemin, poids_couts(self.graphe))
                messagebox.showinfo("Résultat", f"Chemin optimal : {chemin}\nTemps : {temps} h\nCoûts : {couts} UM")
            elif choix_optimisation == 3:
                chemin = optimiser_le_parcours_aller_retour(poids_temps_couts(self.graphe), villes_a_visiter)
                temps = temps_sur_un_chemin(chemin, poids_temps(self.graphe))
                couts = couts_sur_un_chemin(chemin, poids_couts(self.graphe))
                messagebox.showinfo("Résultat", f"Chemin optimal : {chemin}\nTemps : {temps} h\nCoûts : {couts} UM")
        else:
            messagebox.showerror("Erreur", "Choix de voyage invalide")

# Le reste de votre code reste inchangé
Graphe = 'Graphe.txt'
graphe = importer_graphe(Graphe)

interface_root = tk.Tk()
interface = InterfaceGraphique(interface_root, graphe)
interface_root.mainloop()