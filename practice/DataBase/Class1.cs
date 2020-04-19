using System;
using System.Linq;
using System.Collections.Generic;
using System.ComponentModel;
using Dapper;
using Dapper.Contrib.Extensions;

namespace DataBase
{
    [Table("Tasks")]
    public class Task<ID>
    {
        //public Task()
        //{
        //    this.Summary = "";
        //    this.CreatedAt = DateTimeOffset.Now;
        //    this.UpdatedAt = this.CreatedAt;
        //}
        public Task(ID taskId, string summary)
        {
            this.Id = taskId;
            this.Summary = summary;
            this.CreatedAt = DateTimeOffset.Now;
            this.UpdatedAt = this.CreatedAt;
        }

        public Task(ID task_id, string summary, string? description, int? length, DateTimeOffset? deadline, double isCompleted, string status, int? priority, string? location, DateTimeOffset createdAt, DateTimeOffset updatedAt)
        {
            this.Id = task_id;
            this.Summary = summary;
            this.Description = description;
            this.Length = length;
            this.Deadline = deadline;
            this.IsCompleted = isCompleted;
            this.Status = status;
            this.Priority = priority;
            this.Location = location;
            this.CreatedAt = createdAt;
            this.UpdatedAt = updatedAt;
        }

        // property更新時に、UpdatedAtを更新する必要があるが、その昨日は現時点では実装しない。
        // MVVMに組み込むときに考慮する。
        public ID Id { get; }
        public string Summary { get; set; }
        public string? Description { get; set; } = null;
        public int? Length { get; set; } = null;
        public DateTimeOffset? Deadline { get; set; } = null;
        public double IsCompleted { get; set; } = 0.0;
        public string Status { get; set; } = "active";
        public int? Priority { get; set; } = null;
        public string? Location { get; set; } = null;
        public DateTimeOffset CreatedAt { get; }
        public DateTimeOffset UpdatedAt { get; private set; }

    }



    public class DataBase<Connection, TaskID>
              where Connection : System.Data.IDbConnection
    {
        public DataBase(Connection connection)
        {
            this._connection = connection;

            //tableがなければ作成する
            foreach (string query in _table_query)
            {
                _ = this._connection.Execute(sql: query);
            }

        }

        public void Add(Task<TaskID> task)
        {
            string query = @"insert into Tasks values(@Id,@Summary,@Description,@Length,@Deadline,@IsCompleted,@Status,@Priority,@Location,@CreatedAt,@UpdatedAt)";
            this._connection.Execute(query, new
            {
                task.Id,
                task.Summary,
                task.Description,
                task.Length,
                Deadline = task.Deadline?.ToUnixTimeSeconds(),
                task.IsCompleted,
                task.Status,
                task.Priority,
                task.Location,
                CreatedAt = task.CreatedAt.ToUnixTimeSeconds(),
                UpdatedAt = task.UpdatedAt.ToUnixTimeSeconds(),


            });
        }
        public void Add(string summary)
        {
            string query = @"insert into Tasks(Summary,CreatedAt,UpdatedAt) values(@Summary,@CreatedAt,@UpdatedAt)";
            long nowTime = DateTimeOffset.Now.ToUnixTimeSeconds();
            this._connection.Execute(query, new
            {
                Summary=summary,
                CreatedAt = nowTime,
                UpdatedAt = nowTime,
            });
        }

        public List<Task<TaskID>> Get(TaskID id)
        {
            string query = @"select * from Tasks";

            return this._connection.Query(query).ToList().ConvertAll(
                    x =>
                    {
                        //時刻の変換を行う
                        var createdAt = DateTimeOffset.FromUnixTimeSeconds(x.CreatedAt);
                        var updatedAt = DateTimeOffset.FromUnixTimeSeconds(x.UpdatedAt);
                        DateTimeOffset? deadline = null;
                        if (x.Deadline is long temp)
                        {
                             deadline = DateTimeOffset.FromUnixTimeSeconds(temp);
                        }
                        return new Task<TaskID>(
                                 (TaskID)x.Id,
                                 x.Summary,
                                 x.Description,
                                 x.Length,
                                 deadline,
                                 x.IsCompleted,
                                 x.Status,
                                 x.Priority,
                                 x.Location,
                                 createdAt,
                                 updatedAt
                                 );
                    });

        }

        private Connection _connection;

        // tasksのtable生成用query
        private static readonly string[] _table_query = new[]
        {
            "create table if not exists Tasks( Id integer not null primary key autoincrement, Summary text not null, Description text, Length integer, Deadline integer, IsCompleted real,  Status text, Priority integer, Location text, CreatedAt integer not null, UpdatedAt integer not null);",
            "create table if not exists Projects( Id integer not null primary key autoincrement, Name text not null, Begin integer,End integer,Status text,Priority integer,CreatedAt integer not null,UpdatedAt integer not null );",
            "create table if not exists Records( Id integer not null primary key autoincrement, IsCompleted integer not null default 0 check(IsCompleted in (0,1)),Begin integer, End integer,TaskId integer not null, Location text, CommitMessage text not null, foreign key(TaskId) references Tasks(Id));",
            "create table if not exists ReferencePaths( Id integer not null primary key autoincrement, Path text not null );",

            "create table if not exists ProjectReferencing( ProjectId integer,ReferenceId integer,foreign key(ProjectId) references Projects(Id), foreign key(ReferenceId) references ReferencePaths(Id));",
            "create table if not exists TaskBelonging( TaskId integer,ProjectId integer, foreign key(TaskId) references Tasks(Id),foreign key(ProjectId) references Projects(Id));",

            "create table if not exists Tags( Id integer not null primary key autoincrement, Name text unigue not null );",
            "create table if not exists TaskTagging( TaskId integer, TagId integer, foreign key(TaskId) references Tasks(Id), foreign key(TagId) references Tags(Id) );",
            "create table if not exists ProjectTagging( ProjectId integer, TagId integer, foreign key(ProjectId) references Projects(Id), foreign key(TagId) references Tags(Id) );",
            "create table if not exists RecordTagging( RecordId integer, TagId integer, foreign key(RecordId) references Records(Id), foreign key(TagId) references Tags(Id) )",
        };
    }
}
