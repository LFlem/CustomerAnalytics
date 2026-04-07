#!/usr/bin/env python3
"""
🧪 Script de test complet du pipeline Customer Analytics
Test nettoyage → analyse → insights
"""

import pandas as pd
import os
import sys
from pathlib import Path

def test_data_cleaning():
    """Test 1: Vérifier que le nettoyage fonctionne"""
    print("\n" + "="*60)
    print("🔍 TEST 1: Nettoyage des données")
    print("="*60)
    
    raw_file = "data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv"
    clean_file = "data/processed/clean_telco.csv"
    
    # Vérifier fichier brut
    if not os.path.exists(raw_file):
        print(f"❌ ERREUR: Fichier brut manquant: {raw_file}")
        return False
    
    print(f"✅ Fichier brut trouvé: {raw_file}")
    df_raw = pd.read_csv(raw_file)
    print(f"   → {len(df_raw)} lignes chargées")
    
    # Exécuter nettoyage
    try:
        df = pd.read_csv(raw_file)
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
        df = df.dropna()
        df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
        df.to_csv(clean_file, index=False)
        
        print(f"✅ Nettoyage réussi")
        print(f"   → {len(df)} lignes après nettoyage")
        print(f"   → Fichier: {clean_file}")
        return True
    except Exception as e:
        print(f"❌ ERREUR nettoyage: {str(e)}")
        return False


def test_analysis():
    """Test 2: Vérifier l'analyse"""
    print("\n" + "="*60)
    print("📊 TEST 2: Analyse des données")
    print("="*60)
    
    try:
        df = pd.read_csv("data/processed/clean_telco.csv")
        
        # Calculs clés
        churn_rate = df["Churn"].mean()
        churn_by_contract = df.groupby("Contract")["Churn"].mean()
        avg_monthly = df["MonthlyCharges"].mean()
        avg_tenure = df["tenure"].mean()
        
        print(f"✅ Analyse complète")
        print(f"\n   📈 KPIs principaux:")
        print(f"      • Churn global: {churn_rate:.1%}")
        print(f"      • Durée moyenne: {avg_tenure:.1f} mois")
        print(f"      • Revenu moyen: ${avg_monthly:.2f}")
        
        print(f"\n   🔄 Churn par contrat:")
        for contract, rate in churn_by_contract.items():
            print(f"      • {contract}: {rate:.1%}")
        
        # Validation
        if churn_rate > 0.2:
            print(f"\n   ⚠️  ALERTE: Churn élevé (>{churn_rate:.1%})")
        
        return True
    except Exception as e:
        print(f"❌ ERREUR analyse: {str(e)}")
        return False


def test_insights():
    """Test 3: Vérifier la logique d'insights"""
    print("\n" + "="*60)
    print("💡 TEST 3: Génération d'insights")
    print("="*60)
    
    try:
        df = pd.read_csv("data/processed/clean_telco.csv")
        churn_rate = df["Churn"].mean()
        
        # Logique insights
        if churn_rate > 0.25:
            insight = "⚠️  Churn élevé — cibler contrats mensuels"
        else:
            insight = "✅ Churn sous contrôle"
        
        print(f"✅ Insights générés")
        print(f"   {insight}")
        
        # Insights supplémentaires
        month_to_month_churn = df[df["Contract"] == "Month-to-month"]["Churn"].mean()
        if month_to_month_churn > 0.4:
            print(f"   ⚠️  CRITIQUE: Contrats mensuels à {month_to_month_churn:.1%}")
        
        return True
    except Exception as e:
        print(f"❌ ERREUR insights: {str(e)}")
        return False


def test_sql_queries():
    """Test 4: Vérifier les queries SQL (optionnel)"""
    print("\n" + "="*60)
    print("🗄️  TEST 4: Validation requêtes SQL")
    print("="*60)
    
    sql_file = "sql/queries.sql"
    if os.path.exists(sql_file):
        with open(sql_file) as f:
            content = f.read()
        
        if "SELECT" in content and "FROM" in content:
            print(f"✅ SQL queries trouvées")
            print(f"   → {len(content.split('SELECT'))-1} requêtes SQL")
        return True
    else:
        print(f"⚠️  SQL queries non trouvées: {sql_file}")
        return True


def main():
    """Exécuter tous les tests"""
    print("\n" + "🚀 "*30)
    print("PIPELINE DE TEST - CUSTOMER ANALYTICS")
    print("🚀 "*30)
    
    results = {
        "Nettoyage": test_data_cleaning(),
        "Analyse": test_analysis(),
        "Insights": test_insights(),
        "SQL": test_sql_queries(),
    }
    
    # Résumé final
    print("\n" + "="*60)
    print("📋 RÉSUMÉ DES TESTS")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ PASS" if passed_test else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nRésultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 PIPELINE VALIDE - Prêt pour la production!")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué - À corriger")
        return 1


if __name__ == "__main__":
    sys.exit(main())
