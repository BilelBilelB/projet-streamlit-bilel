import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Les prénoms en France", layout="wide")


@st.cache_data
def charger_donnees():
    df = pd.read_csv("data/prenoms-2024-nat.zip", sep=";", keep_default_na=False)
    df["prenom"] = df["prenom"].str.strip()
    lignes = len(df)
    manquants = df.eq("").sum().rename("Valeurs manquantes")

    valides = (
        df["sexe"].isin([1, 2])
        & df["periode"].between(1900, 2024)
        & df["valeur"].gt(0)
        & df["prenom"].ne("")
    )
    invalides = int((~valides).sum())
    df = df.loc[valides].copy()
    doublons = int(df.duplicated().sum())
    df = df.drop_duplicates()
    bilan = pd.DataFrame({
        "Contrôle": ["Lignes brutes", "Lignes invalides retirées",
                     "Doublons retirés", "Lignes conservées"],
        "Nombre": [lignes, invalides, doublons, len(df)]
    })
    return df, manquants, bilan


st.title("Les prénoms en France: des modes qui changent")
st.write(
    "Comment les prénoms les plus donnés changent-ils au fil des générations ? "
    "Ce tableau de bord est pour les étudiants et les personnes curieuses "
    "des tendances démographiques."
)
st.caption("Source : Insee, fichier national 1900-2024, édition 2025.")
donnees, manquants, bilan = charger_donnees()

with st.sidebar:
    st.header("Filtres")
    sexe = st.selectbox("Sexe à la naissance", ["Féminin", "Masculin"])
    debut, fin = st.slider("Période de naissance", 1900, 2024, (1980, 2024))

code_sexe = 2 if sexe == "Féminin" else 1
df = donnees.loc[
    (donnees["sexe"] == code_sexe) & donnees["periode"].between(debut, fin)
].copy()

classement = df.groupby("prenom", as_index=False)["valeur"].sum()
classement = classement.sort_values(["valeur", "prenom"], ascending=[False, True])
total = int(df["valeur"].sum())
leader = classement.iloc[0]["prenom"]

c1, c2, c3 = st.columns(3)
c1.metric("Attributions publiées (arrondies)", total)
c2.metric("Prénoms distincts publiés", df["prenom"].nunique())
c3.metric("Prénom le plus donné sur la période", leader)

st.subheader("1) Quels prénoms dominent la période ?")
st.write(f"{leader} arrive en tête sur la période {debut}-{fin} ({sexe.lower()}).")
top = classement.head(10).sort_values(["valeur", "prenom"])
fig = px.bar(
    top, x="valeur", y="prenom", orientation="h",
    labels={"valeur": "Attributions publiées (arrondi)", "prenom": "Prénom"}
)
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Longueur des barres: effectif cumulé sur la période. On peut survoler pour lire les valeurs. "
    "Les égalités sont départagées par ordre alphabétique."
)

st.subheader("2) Les dix premiers prénoms occupent-ils la même place?")
annuel = df.groupby("periode")["valeur"].sum()
top_annuel = df.sort_values("valeur", ascending=False).groupby("periode").head(10)
concentration = (
    100 * top_annuel.groupby("periode")["valeur"].sum() / annuel
).rename("part").reset_index()
premiere = concentration.iloc[0]["part"]
derniere = concentration.iloc[-1]["part"]
st.write(
    f"La part du top 10 passe de {premiere:.1f} % en {debut} "
    f"à {derniere:.1f} % en {fin}."
)
fig = px.line(
    concentration, x="periode", y="part", markers=True,
    labels={"periode": "Année de naissance", "part": "Part du top 10 (%)"}
)
fig.update_yaxes(rangemode="tozero")
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Le top 10 est recalculé chaque année."
)

st.subheader("3) Un prénom populaire le reste-t-il?")
choix = st.multiselect(
    "Prénoms à comparer (jusqu'à 4)", sorted(df["prenom"].unique()),
    default=classement.head(3)["prenom"].tolist(), max_selections=4
)
if choix:
    grille = pd.MultiIndex.from_product(
        [choix, range(debut, fin + 1)], names=["prenom", "periode"]
    )
    comparaison = (
        df.loc[df["prenom"].isin(choix)].set_index(["prenom", "periode"])
        .reindex(grille).reset_index()
    )
    comparaison["part"] = 100 * comparaison["valeur"] / comparaison["periode"].map(annuel)
    fig = px.line(
        comparaison.sort_values("periode"), x="periode", y="part",
        facet_col="prenom", facet_col_wrap=2, markers=True,
        labels={"periode": "Année de naissance", "part": "Part publiée (%)"}
    )
    fig.update_yaxes(rangemode="tozero")
    st.plotly_chart(fig, use_container_width=True)
st.caption(
    "Petits graphiques sur une même échelle: part annuelle de chaque prénom. "
    "Une année absente reste manquante et n'est pas remplacée par zéro."
)

st.subheader("Ce qu'on peut retenir")
st.write(
    f"La variation de la part du top 10 entre {debut} et {fin} "
    f"est de {derniere - premiere:+.1f} points de pourcentage. "
    "Une baisse signifie que les prénoms dominants occupent une moins grande place "
    "dans les attributions publiées; une hausse montre l'inverse."
)
st.write(
    "Pour comprendre une mode, il faut donc comparer les évolutions annuelles, "
    "pas seulement les classements cumulés. Ces données ne permettent pas "
    "d'expliquer les causes des tendances ni de prédire les modes futures."
)

with st.expander("Qualité des données, méthode et limites"):
    st.write("Contrôles sur le fichier complet, avant les filtres:")
    st.dataframe(bilan, hide_index=True)
    st.dataframe(manquants)
    st.write(
        "Nettoyage: espaces aux extrémités des prénoms retirés "
        "et suppression des doublons. Validation : sexe 1 ou 2, année de 1900 à 2024, "
        "prénom non vide et effectif positif. Les lignes invalides sont exclues. "
        "Aucune valeur manquante n'est estimée."
    )
    st.write(
        "Les effectifs sont arrondis au multiple de 5. Les prénoms attribués moins "
        "de 3 fois par sexe et par année ne sont pas publiés. Les totaux affichés "
        "ne sont donc pas les totaux officiels des naissances."
    )
    st.write(
        "Le fichier concerne le premier prénom des personnes nées en France, "
        "pas la population vivante. Mayotte est incluse depuis 2012. Les données "
        "avant 1946 sont moins complètes."
    )
    st.markdown(
        "[data.gouv.fr](https://www.data.gouv.fr/datasets/fichier-des-prenoms-depuis-1900) · "
        "[Fichier Insee](https://www.insee.fr/fr/statistiques/8894961) · "
        "[Documentation](https://www.insee.fr/fr/statistiques/8894974) · "
        "[Licence Ouverte 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence/)"
    )
