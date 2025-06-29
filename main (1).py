
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


def main():
    # 1. Connect to database
    print("\n1. Connecting to database...")
    conn = sqlite3.connect("database.sqlite")
    cursor = conn.cursor()
    print("✅ Database connected successfully")

    # 2. SELECT operation - Get recent matches
    print("\n2. Fetching recent matches...")
    cursor.execute("""
        SELECT date, home_team_goal, away_team_goal 
        FROM Match 
        WHERE date > '2015-01-01' 
        ORDER BY date DESC 
        LIMIT 10
    """)
    recent_matches = cursor.fetchall()
    print("\nLast 10 matches since 2015:")
    for match in recent_matches:
        print(f"Date: {match[0]}, Score: {match[1]}-{match[2]}")
    # კომენტარი: აჩვენებს ბოლო 10 მატჩს 2015 წლიდან, თარიღით და ანგარიშით

    # 3. INSERT operation - Add new match
    print("\n3. Adding new match...")
    try:
        match_date = input("Enter match date (YYYY-MM-DD): ")
        home_goals = int(input("Home team goals: "))
        away_goals = int(input("Away team goals: "))

        cursor.execute("""
            INSERT INTO Match (date, home_team_goal, away_team_goal, league_id, season, stage, referee) 
            VALUES (?, ?, ?, 1, '2019/2020', 1, 'Unknown')
        """, (match_date, home_goals, away_goals))
        conn.commit()
        print("✅ Match added successfully")
        # კომენტარი: მომხმარებლის მიერ შეყვანილი მატჩი ემატება Match ცხრილში
    except ValueError:
        print("⚠️ Invalid input format")

    # 4. UPDATE operation - Update match
    print("\n4. Updating match...")
    try:
        mid = int(input("Enter match ID to update: "))
        new_home = int(input("New home goals: "))
        new_away = int(input("New away goals: "))

        cursor.execute("""
            UPDATE Match 
            SET home_team_goal = ?, away_team_goal = ? 
            WHERE id = ?
        """, (new_home, new_away, mid))
        conn.commit()
        print("✅ Match updated successfully")
        # კომენტარი: არსებული ჩანაწერის გოლები იცვლება ID-ის მიხედვით
    except ValueError:
        print("⚠️ Invalid input format")

    # 5. DELETE operation - Remove match
    print("\n5. Deleting match...")
    try:
        mid = int(input("Enter match ID to delete: "))
        cursor.execute("DELETE FROM Match WHERE id = ?", (mid,))
        conn.commit()
        print("✅ Match deleted successfully")
        # კომენტარი: მოცემული match id-ის მატჩი წაიშლება ცხრილიდან
    except ValueError:
        print("⚠️ Invalid input format")

    # 6. Data visualizations
    print("\n6. Generating visualizations...")

    # Visualization 1: Matches per season (Bar chart)
    df_seas = pd.read_sql("""
        SELECT substr(season,1,4) AS year, COUNT(*) AS cnt 
        FROM Match 
        GROUP BY year
    """, conn)
    plt.figure(figsize=(10, 5))
    plt.bar(df_seas['year'], df_seas['cnt'], color='skyblue')
    plt.title("მატჩების რაოდენობა სეზონების მიხედვით", fontsize=14)
    plt.xlabel("სეზონი", fontsize=12)
    plt.ylabel("მატჩთა რაოდენობა", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    # კომენტარი: დიაგრამა აჩვენებს მატჩების რაოდენობას ყოველ სეზონში

    # Visualization 2: Average goals per match (Line chart)
    df_score = pd.read_sql("""
        SELECT substr(season,1,4) AS year, 
               AVG(home_team_goal + away_team_goal) AS avg_goals 
        FROM Match 
        GROUP BY year
    """, conn)
    plt.figure(figsize=(10, 5))
    plt.plot(df_score['year'], df_score['avg_goals'],
             marker='o', color='green', linewidth=2)
    plt.title("საშუალო გოლები თითო მატჩში", fontsize=14)
    plt.xlabel("სეზონი", fontsize=12)
    plt.ylabel("საშუალო გოლები", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    # კომენტარი: გრაფიკი აჩვენებს გოლების საშუალო რაოდენობის ტრენდს წლების მიხედვით

    # Visualization 3: Top leagues by match count (Pie chart)
    df_league = pd.read_sql("""
        SELECT League.name AS league, COUNT(*) AS cnt 
        FROM Match 
        JOIN League ON Match.league_id = League.id 
        GROUP BY league 
        ORDER BY cnt DESC LIMIT 3
    """, conn)
    plt.figure(figsize=(8, 8))
    plt.pie(df_league['cnt'], labels=df_league['league'],
            autopct='%1.1f%%', startangle=90,
            colors=['#ff9999', '#66b3ff', '#99ff99'])
    plt.title("საუკეთესო 3 ლიგა მატჩების რაოდენობით", fontsize=14)
    plt.tight_layout()
    plt.show()
    # კომენტარი: დიაგრამა აჩვენებს ლიდერ ლიგებს მატჩების რაოდენობის მიხედვით

    # 7. Close connection
    conn.close()
    print("\n❌ Database connection closed")


if __name__ == "__main__":
    main()





