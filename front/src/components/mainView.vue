<template>
  <div>
    <h1 class="my-5">Comparing a database speed</h1>
    <div class="container mx-auto" style="max-width:75vw">
      <div class="row">
        <div
          class="col-md-4 "
          v-for="database in databases"
          :key="database.name"
        >
          <div class="card mb-5">
            <div class="card-body">
              <h5 class="card-title">
                {{ database.name }}
                <img :src="database.imageURL" style="height:30px" />
              </h5>
              <h6 class="card-subtitle mb-3 text-muted">
                Driver : {{ database.driver }}
              </h6>
              <h6 class="card-subtitle mb-4" v-if="database.description">
                {{ database.description }}
              </h6>
              <hr />
              <div class="row">
                <div class="col">Query</div>
                <div class="col">Time</div>
              </div>
              <hr />
              <div
                class="row mb-2"
                v-for="databaseQuery in database.queries"
                :key="databaseQuery"
              >
                <div class="col" v-if="!databaseQuery.line">
                  <button
                    type="button"
                    class="btn btn-primary"
                    :disabled="
                      (databaseQuery.name === 'Drop Table' && secureMode) ||
                        (databaseQuery.name === 'Import Data to Table' &&
                          database.name === 'Ms SQL' &&
                          secureMode) ||
                        testInProgress
                    "
                    @click="
                      sendRequest(
                        database.url,
                        { databaseQuery },
                        databaseQuery.name === 'Drop Table' &&
                          database.name === 'Ms SQL'
                          ? true
                          : false
                      )
                    "
                  >
                    {{ databaseQuery.name }}
                  </button>
                  <p class="text-muted">{{ databaseQuery.description }}</p>
                </div>
                <div class="col my-auto" v-if="!databaseQuery.line">
                  <p
                    v-html="databaseQuery.time"
                    style="font-family:Times New Roman"
                  ></p>
                </div>
                <div class="col" v-if="databaseQuery.line">
                  <hr />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div style="position:fixed;bottom:0px;right:-10px;width:150px">
    <p
      style="border:1px solid rgba(0,0,0,.125);border-radius:.25rem"
      class="text-left px-3 py-2 align-center btn"
      @click="secureMode = !secureMode"
    >
      Secure mode
      <input type="checkbox" v-model="secureMode" />
    </p>
  </div>
</template>

<script>
import Axios from "axios";
import Swal from "sweetalert2";

export default {
  name: "HelloWorld",
  data() {
    return {
      secureMode: true,
      tableData: null,
      apiURL: "http://127.0.0.1:8000",
      testInProgress: false,
      databases: [
        {
          name: "ClickHouse",
          imageURL: "https://cdn.worldvectorlogo.com/logos/clickhouse.svg",
          driver: "clickhouse_driver",
          description:
            "ClickHouse® is a fast open-source OLAP database management system It is column-oriented and allows to generate analytical reports using SQL queries in real-time.",
          url: "/clickhouse",
          queries: [
            {
              name: "Create Table Structure",
              description: "Create database.",
              query: "createTable",
              time: "2.3197 ms"
            },
            {
              name: "Import Data to Table",
              description: "Import data to table from csv file.",
              query: "importData",
              time: "105336.75 ms </br>105.34 sec"
            },
            {
              name: "Export Data to CSV",
              description: "Export data from database to new CSV file.",
              query: "exportData",
              time: "50637.4 ms <br/>50.64 sec"
            },
            {
              name: "Drop Table",
              description: "Drop table with content.",
              query: "dropTable",
              time: "20.32 ms"
            },
            {
              name: "Count Records",
              description: "Total amount of records.",
              query: "countRecords",
              time: "44.28 ms"
            },
            {
              name: "Get all data",
              description: "Get all records from database.",
              query: "Select * from Orders",
              time: "4273.93 ms </br>4.27 sec"
            },
            { line: true },
            {
              name: "Update all data",
              description: "Add 100 to column 'Units Sold' of each row.",
              query:
                "ALTER Table Orders Update `Units Sold` = `Units Sold`+100 WHERE `Order ID` > 0;",
              time: "123.32 ms"
            },
            {
              name: "Sum over column `Units Sold`",
              description: "Sum of all records value of `Units Sold`.",
              query: "Select Sum(`Units Sold`) FROM Orders",
              time: "203.49 ms"
            },

            {
              name: "Count diffrent `Item Type`",
              description:
                "Count all diffrent Item types grouped by Item Type.",
              query: 'select count(*) from Orders group by "Item Type"',
              time: "153.08 ms"
            },
            {
              name: "Select different 'UnitPrice' ordered",
              description:
                "Returns a list of 'UnitPrice' grouped by 'UnitPrice' and ordered.",
              query:
                'select "Unit Price" from Orders group by "Unit Price" order by "Unit Price"',
              time: "45.14 ms"
            }
          ]
        },
        {
          name: "Postgres",
          imageURL:
            "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Postgresql_elephant.svg/1200px-Postgresql_elephant.svg.png",
          driver: "psycopg2",
          description:
            "PostgreSQL is a powerful, open source object-relational database system with over 30 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.",
          url: "/postgres",
          queries: [
            {
              name: "Create Table Structure",
              description: "Create database.",
              query: "createTable",
              time: "0.57 ms"
            },
            {
              name: "Import Data to Table",
              description: "Import data to table from csv file.",
              query: "importData",
              time: "10310.12 ms <br/>10.31 sec"
            },
            {
              name: "Export Data to CSV",
              description: "Export data from database to new CSV file.",
              query: "exportData",
              time: "13748.98 ms <br/>13.75 sec"
            },
            {
              name: "Drop Table",
              description: "Drop table with content.",
              query: "dropTable",
              time: "13.79 ms"
            },
            {
              name: "Count Records",
              description: "Total amount of records.",
              query: "countRecords",
              time: "370.16 ms"
            },
            {
              name: "Get all data",
              description: "Get all records from database.",
              query: "Select * from Orders",
              time: "4469.76 ms <br/>4.47 sec"
            },
            { line: true },

            {
              name: "Update all data",
              description: "Add 100 to column 'Units Sold' of each row.",
              query: 'UPDATE Orders SET "Units Sold" = "Units Sold" + 100',
              time: "23487.09 ms <br/>23.49 sec"
            },
            {
              name: "Sum over column `Units Sold`",
              description: "Sum of all records value of `Units Sold`.",
              query: 'Select SUM("Units Sold") FROM Orders',
              time: "203.49 ms"
            },
            {
              name: "Count diffrent `Item Type`",
              description:
                "Count all diffrent Item types grouped by Item Type.",
              query: 'select count(*) from Orders group by "Item Type"',
              time: "673.58 ms"
            },
            {
              name: "Select different 'UnitPrice' ordered",
              description:
                "Returns a list of 'UnitPrice' grouped by 'UnitPrice' and ordered.",
              query:
                'select "Unit Price" from orders group by "Unit Price" order by "Unit Price"',
              time: "580.75 ms"
            }
          ]
        },
        {
          name: "Ms SQL",
          driver: "pymssql",
          imageURL:
            "https://cdn.worldvectorlogo.com/logos/microsoft-sql-server.svg",
          description:
            "Microsoft SQL Server is a relational database management system developed by Microsoft. As a database server, it is a software product with the primary function of storing and retrieving data as requested.",
          url: "/mssql",
          queries: [
            {
              name: "Create Table Structure",
              description: "Create database.",
              query: "createTable",
              time: "100 ms"
            },
            {
              name: "Import Data to Table",
              description: "Import data to table from csv file.",
              query: "importData",
              time: "~ 40 min"
            },
            {
              name: "Export Data to CSV",
              description: "Export data from database to new CSV file.",
              query: "exportData",
              time: "85303.63 ms <br/>85.3 sec<br/> 1.42 min"
            },
            {
              name: "Drop Table",
              description: "Drop table with content.",
              query: "dropTable",
              time: "You don't want to do this."
            },
            {
              name: "Count Records",
              description: "Total amount of records.",
              query: "countRecords",
              time: "287.0 ms"
            },
            {
              name: "Get all data",
              description: "Get all records from database.",
              query: "Select * from Orders",
              time: "3.63 ms"
            },
            { line: true },
            {
              name: "Update all data",
              description: "Add 100 to column 'Units Sold' of each row.",
              query: 'UPDATE Orders SET "Units Sold" = "Units Sold" + 100',
              time: "37192.46 ms <br/>37.19 sec"
            },
            {
              name: "Sum over column `Units Sold`",
              description: "Sum of all records value of `Units Sold`.",
              query: "Select sum([Units Sold]) FROM Orders",
              time: "283.76 ms"
            },
            {
              name: "Count diffrent `Item Type`",
              description:
                "Count all diffrent Item types grouped by Item Type.",
              query: 'select count(*) from Orders group by "Item Type"',
              time: "900.48 ms"
            },
            {
              name: "Select different 'UnitPrice' ordered",
              description:
                "Returns a list of 'UnitPrice' grouped by 'UnitPrice' and ordered.",
              query:
                "select [Unit Price] from orders group by [Unit Price] order by [Unit Price]",
              time: "153.08 ms"
            }
          ]
        }
      ]
    };
  },
  mounted() {
    // this.getDatabaseData();
  },
  methods: {
    getDatabaseData() {
      this.testInProgress = true;
      Axios.get(this.apiURL + "/clickhouse")
        .then(result => {
          if (result.status == 500 || result.status == 422) {
            Swal.fire({
              toast: true,
              position: "top-end",
              icon: "error",
              timerProgressBar: true,
              html: "<b>Error : </b>'" + result.data.error,
              showConfirmButton: false,
              timer: 3000
            });
          }
          if (result.status == 200) {
            this.tableData = result.data.data;
            let data = "";
            if (this.tableData) data = "<br/><b>Data : </b>" + this.tableData;
            Swal.fire({
              toast: true,
              position: "top-end",
              icon: "success",
              timerProgressBar: true,
              html:
                "<b>Query : </b>'" +
                result.data.query +
                "' <br/><b>Executed in : </b>" +
                result.data.time +
                data,
              showConfirmButton: false,
              timer: 6000
            });
          }
          this.testInProgress = false;
        })
        .catch(error => {
          console.log(error);
          Swal.fire({
            toast: true,
            position: "top-end",
            icon: "error",
            timerProgressBar: true,
            html: "<b>Error : </b>'" + error,
            showConfirmButton: false,
            timer: 6000
          });
        });
    },
    async sendRequest(url, query, confirm = false) {
      let shouldRun = "";
      if (confirm)
        shouldRun = await Swal.fire({
          title: "Are you sure?",
          showCancelButton: true,
          confirmButtonText: `Confirm`
        });
      if (shouldRun.isConfirmed || !confirm) {
        this.testInProgress = true;
        // requestQuery = query.query;
        console.log("query");
        console.log(query);
        console.log(query.databaseQuery.name);
        console.log(query.databaseQuery.query);
        console.log(query.databaseQuery.time);

        let xd = new Swal({
          toast: true,
          position: "top-end",
          icon: "info",
          title: "Please Wait !",
          showConfirmButton: false,
          onBeforeOpen: () => {
            Swal.showLoading();
          }
        });
        await Axios.post(this.apiURL + url, {
          query: query.databaseQuery.query
        })
          .then(result => {
            xd.close();
            // time = result.data.time;
            if (result.status == 200) {
              query.databaseQuery.time = result.data.time;
              let data = "";
              if (result.data.data)
                data = "<br/><b>Data : </b>" + result.data.data;
              Swal.fire({
                toast: true,
                position: "top-end",
                icon: "success",
                timerProgressBar: true,
                html:
                  "<b>Query : </b>'" +
                  result.data.query +
                  data +
                  "' <br/><b>Executed in : </b>" +
                  result.data.time,
                showConfirmButton: false,
                timer: 6000,
                didOpen: toast => {
                  toast.addEventListener("mouseenter", Swal.stopTimer);
                  toast.addEventListener("mouseleave", Swal.resumeTimer);
                }
              });
            } else {
              xd.close();
              Swal.fire({
                toast: true,
                position: "top-end",
                icon: "error",
                timerProgressBar: true,
                html: "<b>Error : </b>'" + result.data.error,
                showConfirmButton: false,
                timer: 6000,
                didOpen: toast => {
                  toast.addEventListener("mouseenter", Swal.stopTimer);
                  toast.addEventListener("mouseleave", Swal.resumeTimer);
                }
              });
            }
            this.testInProgress = false;
          })
          .catch(error => {
            xd.close();
            console.log("error");
            // console.log(error.response.data);
            Swal.fire({
              toast: true,
              position: "top-end",
              icon: "error",
              timerProgressBar: true,
              html: "<b>Error : </b>'" + error.response.data.error,
              showConfirmButton: false,
              timer: 6000,
              didOpen: toast => {
                toast.addEventListener("mouseenter", Swal.stopTimer);
                toast.addEventListener("mouseleave", Swal.resumeTimer);
              }
            });
            this.testInProgress = false;
          });
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
