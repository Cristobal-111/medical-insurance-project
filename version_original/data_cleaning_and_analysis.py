"""
PROYECTO: Limpieza, Validación y Análisis Exploratorio de Datos - Medical Insurance
================================================================================
Objetivo: Limpiar, validar y transformar un dataset de seguros de salud,
y generar visualizaciones que respalden los hallazgos principales.

Proyecto realizado como práctica personal en el marco del
Google Advanced Data Analytics Professional Certificate.

Autor: Cristóbal Rojas Troncoso
GitHub: github.com/Cristobal-111
================================================================================
"""

# PASO 1: IMPORTAR LIBRERÍAS
# ============================================================

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

print("✅ Librerías importadas correctamente\n")

# Configuración general
pd.set_option('display.max_columns', None)
sns.set_theme(style="whitegrid")

# Rutas del proyecto (relativas, para que funcione igual en cualquier PC / GitHub)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMAGES_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

# PASO 2: CARGAR Y EXPLORAR EL DATASET
# ============================================================

insurance = pd.read_csv(os.path.join(DATA_DIR, "insurance.csv"))

print("📊 EXPLORACIÓN INICIAL DEL DATASET")
print("=" * 80)
print(f"\nDimensiones: {insurance.shape[0]} filas × {insurance.shape[1]} columnas")
print(f"Total de valores: {insurance.size:,}\n")

print("Primeras 5 filas:")
print(insurance.head())

print("\n\nTipos de datos:")
print(insurance.dtypes)

print("\n\nEstadísticas descriptivas:")
print(insurance.describe())

print("\n\nValores faltantes por columna:")
print(insurance.isnull().sum())

# PASO 3: IDENTIFICACIÓN DE PROBLEMAS
# ============================================================

print("\n" + "=" * 80)
print("🔍 IDENTIFICACIÓN DE PROBLEMAS EN LOS DATOS")
print("=" * 80)

print("\n1️⃣ FILAS DUPLICADAS:")
duplicates = insurance.duplicated().sum()
print(f"   Número de filas completamente duplicadas: {duplicates}")
if duplicates > 0:
    print("\n   Filas duplicadas encontradas:")
    print(insurance[insurance.duplicated(keep=False)])

print("\n2️⃣ VALORES FALTANTES:")
missing = insurance.isnull().sum()
if missing.sum() > 0:
    print("   Columnas con valores faltantes:")
    print(missing[missing > 0])
else:
    print("   ✅ No hay valores faltantes")

print("\n3️⃣ VALIDACIÓN DE LA COLUMNA 'age' (Edad):")
print(f"   Edad mínima: {insurance['age'].min()}")
print(f"   Edad máxima: {insurance['age'].max()}")
print(f"   ¿Hay edades negativas o inválidas? {(insurance['age'] < 0).any()}")

print("\n4️⃣ VALIDACIÓN DE LA COLUMNA 'bmi' (BMI):")
print(f"   BMI mínimo: {insurance['bmi'].min()}")
print(f"   BMI máximo: {insurance['bmi'].max()}")
print(f"   ¿Hay BMI negativos o cero? {(insurance['bmi'] <= 0).any()}")

print("\n5️⃣ VALIDACIÓN DE COLUMNAS CATEGÓRICAS:")
print("\n   Valores únicos en 'sex':")
print(f"   {insurance['sex'].unique()}")
print(f"   Conteo:\n{insurance['sex'].value_counts()}")

print("\n   Valores únicos en 'smoker':")
print(f"   {insurance['smoker'].unique()}")
print(f"   Conteo:\n{insurance['smoker'].value_counts()}")

print("\n   Valores únicos en 'region':")
print(f"   {insurance['region'].unique()}")
print(f"   Conteo:\n{insurance['region'].value_counts()}")

print("\n6️⃣ VALIDACIÓN DE LA COLUMNA 'charges' (Costo del Seguro):")
print(f"   Costo mínimo: ${insurance['charges'].min():.2f}")
print(f"   Costo máximo: ${insurance['charges'].max():.2f}")
print(f"   ¿Hay costos negativos? {(insurance['charges'] < 0).any()}")

# PASO 4: LIMPIEZA DE DATOS
# ============================================================

print("\n" + "=" * 80)
print("🧹 LIMPIEZA DE DATOS")
print("=" * 80)

insurance_clean = insurance.copy()

print("\n✂️  Eliminando filas duplicadas...")
initial_rows = len(insurance_clean)
insurance_clean = insurance_clean.drop_duplicates()
print(f"   Filas removidas: {initial_rows - len(insurance_clean)}")
print(f"   Filas restantes: {len(insurance_clean)}")

print("\n📝 Estandarizando valores en columnas categóricas...")
insurance_clean['sex'] = insurance_clean['sex'].str.lower()
insurance_clean['smoker'] = insurance_clean['smoker'].str.lower()
insurance_clean['region'] = insurance_clean['region'].str.lower()
print("   ✅ Valores convertidos a minúsculas")

print("\n🗑️  Removiendo valores faltantes...")
initial_rows = len(insurance_clean)
insurance_clean = insurance_clean.dropna()
rows_removed = initial_rows - len(insurance_clean)
print(f"   Filas removidas: {rows_removed}" if rows_removed > 0 else "   ✅ No había valores faltantes")

# PASO 5: VALIDACIÓN POST-LIMPIEZA
# ============================================================

print("\n" + "=" * 80)
print("✅ VALIDACIÓN POST-LIMPIEZA")
print("=" * 80)
print(f"\nDimensiones finales: {insurance_clean.shape[0]} filas × {insurance_clean.shape[1]} columnas")
print(f"Duplicados restantes: {insurance_clean.duplicated().sum()}")
print(f"Valores faltantes: {insurance_clean.isnull().sum().sum()}")

# PASO 6: CONVERSIÓN DE VARIABLES CATEGÓRICAS A NUMÉRICAS
# ============================================================

print("\n" + "=" * 80)
print("🔢 CONVERSIÓN DE VARIABLES CATEGÓRICAS A NUMÉRICAS")
print("=" * 80)

insurance_transformed = insurance_clean.copy()

print("\n1️⃣ Codificando 'sex' (Label Encoding - Nominal):")
sex_mapping = {'male': 0, 'female': 1}
insurance_transformed['sex_encoded'] = insurance_transformed['sex'].map(sex_mapping)
print(f"   Mapeo: {sex_mapping}")

print("\n2️⃣ Codificando 'smoker' (Label Encoding - Nominal):")
smoker_mapping = {'no': 0, 'yes': 1}
insurance_transformed['smoker_encoded'] = insurance_transformed['smoker'].map(smoker_mapping)
print(f"   Mapeo: {smoker_mapping}")

print("\n3️⃣ Codificando 'region' (Label Encoding - Nominal):")
region_unique = insurance_transformed['region'].unique()
region_mapping = {region: idx for idx, region in enumerate(sorted(region_unique))}
insurance_transformed['region_encoded'] = insurance_transformed['region'].map(region_mapping)
print(f"   Mapeo: {region_mapping}")

print("\n4️⃣ Crear variable derivada 'age_group':")
insurance_transformed['age_group'] = insurance_transformed['age'].apply(
    lambda x: 'young' if x < 30 else 'middle' if x < 50 else 'senior'
)
print(insurance_transformed['age_group'].value_counts())

print("\n5️⃣ One-Hot Encoding para 'region':")
region_dummies = pd.get_dummies(insurance_transformed['region'], prefix='region')
insurance_transformed = pd.concat([insurance_transformed, region_dummies], axis=1)
print(f"   Nuevas columnas creadas: {list(region_dummies.columns)}")

# PASO 7: GUARDAR DATASET LIMPIO
# ============================================================

output_csv = os.path.join(DATA_DIR, "insurance_cleaned.csv")
insurance_transformed.to_csv(output_csv, index=False)
print(f"\n✅ Dataset limpio guardado en: {output_csv}")

# PASO 8: ANÁLISIS Y VISUALIZACIONES
# ============================================================

print("\n" + "=" * 80)
print("📈 GENERANDO VISUALIZACIONES")
print("=" * 80)

# 1. Distribución de charges
plt.figure(figsize=(8, 5))
sns.histplot(insurance_transformed['charges'], bins=40, kde=True, color="#2E86AB")
plt.title("Distribución del costo del seguro (charges)")
plt.xlabel("Costo del seguro ($)")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "01_distribucion_charges.png"), dpi=150)
plt.close()

# 2. Charges por fumador vs no fumador (boxplot)
plt.figure(figsize=(7, 5))
sns.boxplot(data=insurance_transformed, x='smoker', y='charges', hue='smoker',
            palette=["#2E86AB", "#E74C3C"], legend=False)
plt.title("Costo del seguro: Fumadores vs No fumadores")
plt.xlabel("¿Fuma?")
plt.ylabel("Costo del seguro ($)")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "02_charges_por_fumador.png"), dpi=150)
plt.close()

# 3. Relación edad vs charges, coloreado por fumador
plt.figure(figsize=(8, 5))
sns.scatterplot(data=insurance_transformed, x='age', y='charges', hue='smoker',
                 palette=["#2E86AB", "#E74C3C"], alpha=0.7)
plt.title("Relación entre edad y costo del seguro, según hábito de fumar")
plt.xlabel("Edad")
plt.ylabel("Costo del seguro ($)")
plt.legend(title="Fumador")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "03_edad_vs_charges.png"), dpi=150)
plt.close()

# 4. BMI vs charges
plt.figure(figsize=(8, 5))
sns.scatterplot(data=insurance_transformed, x='bmi', y='charges', hue='smoker',
                 palette=["#2E86AB", "#E74C3C"], alpha=0.7)
plt.title("Relación entre BMI y costo del seguro, según hábito de fumar")
plt.xlabel("BMI (Índice de Masa Corporal)")
plt.ylabel("Costo del seguro ($)")
plt.legend(title="Fumador")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "04_bmi_vs_charges.png"), dpi=150)
plt.close()

# 5. Costo promedio por región
plt.figure(figsize=(8, 5))
region_avg = insurance_transformed.groupby('region')['charges'].mean().sort_values()
sns.barplot(x=region_avg.index, y=region_avg.values, hue=region_avg.index,
            palette="Blues_d", legend=False)
plt.title("Costo promedio del seguro por región")
plt.xlabel("Región")
plt.ylabel("Costo promedio ($)")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "05_costo_promedio_region.png"), dpi=150)
plt.close()

# 6. Costo promedio por grupo etario
plt.figure(figsize=(8, 5))
age_order = ['young', 'middle', 'senior']
age_avg = insurance_transformed.groupby('age_group')['charges'].mean().reindex(age_order)
sns.barplot(x=age_avg.index, y=age_avg.values, hue=age_avg.index,
            palette="Oranges_d", legend=False)
plt.title("Costo promedio del seguro por grupo etario")
plt.xlabel("Grupo etario")
plt.ylabel("Costo promedio ($)")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "06_costo_promedio_edad.png"), dpi=150)
plt.close()

# 7. Matriz de correlación (variables numéricas)
plt.figure(figsize=(8, 6))
corr_cols = ['age', 'bmi', 'children', 'charges', 'sex_encoded', 'smoker_encoded', 'region_encoded']
corr = insurance_transformed[corr_cols].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Matriz de correlación entre variables")
plt.tight_layout()
plt.savefig(os.path.join(IMAGES_DIR, "07_matriz_correlacion.png"), dpi=150)
plt.close()

print(f"   ✅ 7 gráficos guardados en: {IMAGES_DIR}")

# PASO 9: INSIGHTS FINALES
# ============================================================

print("\n" + "=" * 80)
print("📈 ANÁLISIS FINAL - INSIGHTS")
print("=" * 80)

print("\n1️⃣ Distribución por género:")
print(insurance_transformed['sex'].value_counts())

smoker_pct = (insurance_transformed['smoker_encoded'].sum() / len(insurance_transformed)) * 100
print(f"\n2️⃣ Proporción de fumadores: {smoker_pct:.1f}%")

print("\n3️⃣ Costo promedio por grupo de edad:")
print(insurance_transformed.groupby('age_group')['charges'].mean().round(2))

print("\n4️⃣ Costo promedio: Fumadores vs No Fumadores:")
print(insurance_transformed.groupby('smoker')['charges'].mean().round(2))

print("\n5️⃣ Correlación de 'smoker' con 'charges':")
print(f"   {corr.loc['smoker_encoded', 'charges']:.3f}")

print("\n" + "=" * 80)
print("✅ ¡PROYECTO COMPLETADO!")
print("=" * 80)
print(f"\n📁 Dataset limpio: {output_csv}")
print(f"📁 Gráficos: {IMAGES_DIR}")
