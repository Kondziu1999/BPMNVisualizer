<template>
  <v-app id="app">
    <LeftPanel
               :fileConfirmed="fileConfirmed"
               v-on:editFile="editFile"
               v-on:applyFilter="applyFilter"
               :route="route"
               v-on:setRoute="setRoute">
    </LeftPanel>

    <v-main id="mainDiv">

      <SelectFile
          v-if="route==='FILE'"
          v-on:confirmFile="confirmFile"
          v-on:removeFile="removeFile"
          :columnsConfirmedString="columnsConfirmedString">
      </SelectFile>

      <ChartContent
          v-if="route==='CHART'"
          :fileData="fileData"
          :columnsConfirmedString="columnsConfirmedString">
      </ChartContent>
    </v-main>
  </v-app>
</template>

<script>
import LeftPanel from './components/LeftPanel.vue';
import ChartContent from './components/routes/ChartContent.vue';
import SelectFile from "./components/routes/SelectFile";

export default {
  name: 'App',
  components: {
    LeftPanel,
    SelectFile,
    ChartContent
  },
  methods: {
    confirmFile: function (fileData, columnsConfirmedString) {
      this.fileData = fileData;
      this.columnsConfirmedString = columnsConfirmedString;
      this.fileConfirmed = true
    },
    removeFile: function () {
      this.fileConfirmed = false
    },
    editFile: function () {
      this.fileConfirmed = false;
    },
    applyFilter: function (minNodeValue) {
      this.minNodeValue = minNodeValue;
    },
    setRoute: function (newRoute) {
      this.route = newRoute;
    }
  },
  data() {
    return {
      route: 'FILE',
      fileConfirmed: false,
      fileData: undefined,
      columnsConfirmedString: 'Case ID,Activity,Start Timestamp',
      minNodeValue: 0
    }
  }

}
</script>

<style>

.v-application {
  background-color: #eaeaea;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.div-inline {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

#mainDiv {
  margin-left: 350px;
  top: 10px;
}

.input {
  min-width: 500px;
  padding: 12px 20px;
  margin: 8px;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
