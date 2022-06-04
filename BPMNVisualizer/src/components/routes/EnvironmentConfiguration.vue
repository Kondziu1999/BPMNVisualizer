<template>
  <h1>BPMN visualizer</h1>

  <p>
    Narzędzie do wizualizacji i przetwarzania procesów
  </p>

  <h3>
    Konfiguracja
  </h3>

  <p>
    - BPMN visualizer wymaga podłączenia serwera backendowego wykonującego obliczenia.
    Można go zbudować ręcznie klonując repozytorium: <a href="https://github.com/Kondziu1999/BPMNVisualizer">repo</a>
    Lub użyć standalone wersji dostępnej w formie notatnika:
    <a href="https://colab.research.google.com/drive/1aDX4EDf2q1gBQPZVTMm2HsqIH1SMwpj9?usp=sharing">link</a>
  </p>

  <div>
    <h3>Skonfiguruj adres środowiska obliczeniowgo</h3>
    <input v-model="backendUrl" placeholder="Rest endpoint URL" class="input">
    <v-btn @click="checkConnection"
           class="text-white"
           color="#34495E">
      Zatwierdź i zweryfikuj połączenie
      <v-icon dark right>
        mdi-checkbox-marked-circle
      </v-icon>
    </v-btn>

    <Alert v-if="!!successMessage" :msg="successMessage" severity="success"></Alert>
    <Alert v-if="!!errorMessage" :msg="errorMessage" severity="error"></Alert>
  </div>
</template>
<script>

import axios from "axios";
import Alert from "../generic/Alert";

export default {
  name: 'EnvironmentConfiguration',
  props: {
    backendConfirmedUrl: String
  },
  data() {
    return {
      backendUrl: this.backendConfirmedUrl,
      successMessage: '',
      errorMessage: ''
    }
  },
  components: {
    Alert
  },
  methods: {
    checkConnection() {
      this.successMessage = '';
      this.errorMessage = '';

      if (this.backendUrl) {
        this.loading = true;
        axios
            .get(`${this.backendUrl}`)
            .then(() => {
                this.$emit('confirmBackend', this.backendUrl)
                this.successMessage = 'Połączenie jest poprawne';
            })
            .catch(err => {
              this.errorMessage = 'Połączenie jest niepoprawne: ' + err.message;
            })
      } else {
        this.errorMessage = 'Podaj adres url';
      }
    }
  }
}
</script>

<style scoped>

h3,h1 {
  margin-top: 30px;
  margin-bottom: 10px;
}

.backend-input {
  min-width: 500px;
  padding: 12px 20px;
  margin: 8px;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}
</style>
