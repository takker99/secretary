using System;
using System.Data.SQLite;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

using ConsoleAppFramework;

using Dapper;
using Dapper.Contrib.Extensions;

using Microsoft.Extensions.Hosting;

namespace HelloDataBase
{

    class Program : ConsoleAppBase
    {
        static async Task Main(string[] args) => await Host.CreateDefaultBuilder().RunConsoleAppFrameworkAsync<Program>(args);
        public void Run([Option("o", "接続するdatabaseへのpath")]string dataSource = @"test.sqlite3")
        {
            Console.Write("Connecting SQLite database...");

            var connectionString = new SQLiteConnectionStringBuilder { DataSource = dataSource };

            using var connection = new SQLiteConnection(connectionString.ToString());
            var database = new DataBase.DataBase<SQLiteConnection, int>(connection);
            Console.WriteLine("done.");
            Console.WriteLine("Inserting a task...");
            database.Add(new DataBase.Task<int>(taskId: 0, summary: "テストを書く"));

            Console.Write("Selecting data...");
            var result = database.Get(0);
            Console.WriteLine("done.");

            foreach (var task in result)
            {
                Console.WriteLine($"{task.Id}, {task.Summary},{task.Deadline}, {task.CreatedAt.LocalDateTime}, {task.UpdatedAt.LocalDateTime}");
            }

            connection.Close();
            Console.WriteLine("Successfully finished!");
        }

        [Command("add")]
        public void AddTask([Option(0)]string? summary = null, [Option("o", "接続するdatabaseへのpath")]string dataSource = @"test.sqlite3")
        {
            Console.Write("Connecting SQLite database...");

            var connectionString = new SQLiteConnectionStringBuilder { DataSource = dataSource };

            using var connection = new SQLiteConnection(connectionString.ToString());
            var database = new DataBase.DataBase<SQLiteConnection, int>(connection);
            Console.WriteLine("done.");
            Console.WriteLine($"database path: {System.IO.Path.GetFullPath(dataSource)}");
            if (summary is null)
            {
                this._addTaskInteractiveMode(database);
            }
            else
            {
                Console.WriteLine("Inserting a task...");
                database.Add(summary);
                Console.WriteLine("done.");
            }

            connection.Close();
            Console.WriteLine("Successfully finished!");
        }

        private void _addTaskInteractiveMode(DataBase.DataBase<SQLiteConnection, int> database)
        {
            Console.WriteLine("Interactive mode.");
            while (true)
            {
                // q keyで終了、a keyでタスク追加
                Console.Write("quit:q add task:a>");
                switch (Console.ReadKey().Key)
                {
                    case ConsoleKey.Q:
                        Console.WriteLine();
                        return;
                    case ConsoleKey.A:
                        Console.WriteLine();
                        Console.Write("Input summary>");
                        string summary = Console.ReadLine().ToString();
                        Console.WriteLine("Inserting a task...");
                        database.Add(summary);
                        Console.WriteLine("done.");
                        break;
                    default:
                        Console.WriteLine();
                        Console.WriteLine("type q or a.");
                        break;
                }
            }
        }
        #region Dapper練習用コード
        private class Denco
        {
            public int Id { get; set; } = 0;
            public string Name { get; set; } = "";
            public string Type { get; set; } = "";
            public string Attribute { get; set; } = "";
            public int MaxAP { get; set; } = 0;
            public int MaxHP { get; set; } = 0;
            public string? Skill { get; set; } = null;
        }
        static private void _test_function1()
        {
            Console.Write("Connecting SQLite database...");

            var connectionString = new SQLiteConnectionStringBuilder { DataSource = @"denco.sqlite3" };

            using var connection = new SQLiteConnection(connectionString.ToString());
            Console.WriteLine("done.");

            Console.Write("Opening SQLite database...");
            connection.Open();
            Console.WriteLine("done.");

            // cf.https://qiita.com/koshian2/items/63938474001c510d0b15#2sqlite3%E3%81%AE%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%B3%E7%A2%BA%E8%AA%8D
            // 上記の例をもとに、DapperでDB操作をしてみる

            //tableを作成する
            Console.Write("Creating table...");
            connection.Execute(@"CREATE TABLE IF NOT EXISTS Dencos(
                    Id INTEGER NOT NULL PRIMARY KEY autoincrement,
                    Name TEXT NOT NULL,
                    Type TEXT NOT NULL,
                    Attribute TEXT NOT NULL,
                    MaxAP INTEGER NOT NULL,
                    MaxHP INTEGER NOT NULL,
                    Skill TEXT);");
            Console.WriteLine("done.");

            // dataを挿入する
            Console.Write("Inserting data...");
            var id = connection.Insert(new Denco[]
                {
                        new Denco
                        {
                            Id = 2,
                            Name = "為栗メロ",
                            Type = "アタッカー",
                            Attribute = "eco",
                            MaxAP = 310,
                            MaxHP = 300,
                            Skill = "きゃのんぱんち"
                        },
                        new Denco
                        {
                            Id = 3,
                            Name = "新阪ルナ",
                            Type = "ディフェンダー",
                            Attribute = "cool",
                            MaxAP = 220,
                            MaxHP = 360,
                            Skill = "ナイトライダー"
                        },
                        new Denco
                        {
                            Id = 4,
                            Name = "恋浜みろく",
                            Type = "トリックスター",
                            Attribute = "heat",
                            MaxAP = 300,
                            MaxHP = 360,
                            Skill = "ダブルアクセス"
                        },
                        new Denco
                        {
                            Id = 8,
                            Name = "天下さや",
                            Type = "アタッカー",
                            Attribute = "cool",
                            MaxAP = 400,
                            MaxHP = 240,
                            Skill = null
                        },
                        new Denco
                        {
                            Id = 13,
                            Name = "新居浜いずな",
                            Type = "ディフェンダー",
                            Attribute = "heat",
                            MaxAP = 290,
                            MaxHP = 336,
                            Skill = "重連壁"
                        },
                        new Denco
                        {
                            Id = 31,
                            Name = "新居浜ありす",
                            Type = "ディフェンダー",
                            Attribute = "heat",
                            MaxAP = 270,
                            MaxHP = 350,
                            Skill = "ハッピーホリデイ"
                        },
                });
            Console.WriteLine("done.");

            //dataを取得する
            //  objectに変換した形で受け取ることができる
            Console.Write("Selecting data...");
            var query = @"SELECT * FROM Dencos WHERE MaxAP >= 300 ORDER BY MaxHP desc";
            var result = connection.Query<Denco>(query);
            Console.WriteLine("done.");


            foreach (var denco in result)
            {
                Console.WriteLine($"{denco.Id}, {denco.Name}, {denco.Type}, {denco.Attribute}, {denco.MaxAP}, {denco.MaxHP}, {denco.Skill}");
            }

            connection.Close();

            Console.WriteLine("Successfully finished!");
        }

        // cf.http://neue.cc/2012/12/11_390.html
        // snake_caseのDBのsymbolを、PascalCaseのC#のsymbolに置き換える
        private static void _setSnakeToPascal<T>()
        {
            var mapper = new CustomPropertyTypeMap(typeof(T), (type, columnName) =>
            {
                //snake_caseをPascalCaseに変換
                string propName = Regex.Replace(columnName, @"^(.)|_(\w)", x => x.Groups[1].Value.ToUpper() + x.Groups[2].Value.ToUpper());
                return type.GetProperty(propName);
            });

            SqlMapper.SetTypeMap(typeof(T), mapper);
        }
        #endregion
    }
}
