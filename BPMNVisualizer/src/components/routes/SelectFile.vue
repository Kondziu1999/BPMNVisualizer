<template>
  <div>
    <h3>Wybierz plik</h3>

    <input type="file" @change="previewFile">

    <h3>Kolumny</h3>

    <div v-if="isCsv">
      <label>
        Podaj nazwy kolumn
        <input v-model="currentColumn"
               placeholder="nazwa kolumny" class="input">
      </label>

        <v-btn
          elevation="2"
          fab
          x-small
          @click="addColumn"
          class="text-white"
          color="#34495E"
        >
        <v-icon dark>
          mdi-plus
        </v-icon>
      </v-btn>

      <p>
        Wybrane kolumny
      </p>
      <ol>
        <li v-for="col in columnsList" :key="col">
          {{ col }}
          <v-btn
            elevation="2"
            icon
            x-small
            @click="removeColumn(col)"
            class="text-white"
            style="height: 30px;width: 30px"
            color="#34495E"
          >
            <v-icon dark>
              mdi-minus
            </v-icon>
          </v-btn>
        </li>
      </ol>
    </div>
    <h3>Zatwierdź</h3>
    <v-btn @click="confirmFile"
           class="text-white"
           color="#34495E"
    >
      Zapisz
      <v-icon dark right>
        mdi-checkbox-marked-circle
      </v-icon>
    </v-btn>

    <Alert v-if="!!invalidMessage" :msg="invalidMessage" severity="error"></Alert>

  </div>
</template>

<script>
import Alert from "@/components/generic/Alert";
export default {
  name: 'SelectFile',
  components: {Alert},
  props: {
    columnsConfirmedString: String,
  },
  data() {
    return {
      isCsv: false,
      fileData: File,
      currentColumn: "",
      columns: this.columnsConfirmedString.split(','),
      invalidMessage: this.invalidMessage,
    }
  },
  computed: {
    columnsList() {
      return this.columns ?? [];
    }
  },
  methods: {
    addColumn() {
      this.columns.push(this.currentColumn);
    },
    removeColumn(column) {
      this.columns = this.columns.filter(x => x !== column);
    },
    previewFile(event) {
      const file = event.target.files[0];
      if (file) {
        this.fileData = file;

        if (file.name.split('.')[1] === "csv") {
          this.isCsv = true;
        }
        else {
          this.isCsv = false;
        }
      }
      else{
        this.fileData = undefined;
        this.$emit('removeFile')
      }
    },
    confirmFile: function () {
      if (!this.fileData) {
        this.invalidMessage = "Nie wybrano pliku";
        console.log(this.invalidMessage);
        return;
      }
      if (!this.columns.length) {
        this.invalidMessage = "Nie podano znaczenia kolumn";
        console.log(this.invalidMessage);
        return;
      }

      this.invalidMessage = undefined;

      this.$emit('confirmFile', this.fileData, this.columns.join(','))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

h3 {
  margin-top: 30px;
  margin-bottom: 10px;
}

ol {
  padding-left: 50px;
}

</style>
