<template>
  <div>
    <h3>
      Filtry
    </h3>
    <label>
      Minimalna ilość wystąpień eventu
      <input v-model="minNodeValue" placeholder="0" class="input" type="number" id="minNodeValueFilter">
      <v-btn
          elevation="2"
          icon
          x-small
          @click="minNodeValue--"
          class="text-white"
          style="height: 30px;width: 30px"
          color="#34495E"
      >
        <v-icon dark>
          mdi-minus
        </v-icon>
      </v-btn>

      <v-btn
          elevation="2"
          icon
          x-small
          @click="minNodeValue++"
          class="text-white"
          style="height: 30px;width: 30px"
          color="#34495E"
      >
        <v-icon dark>
          mdi-plus
        </v-icon>
      </v-btn>

    </label>

    <div class="div-inline">
      <h3>Wygenerowany BPN</h3>
    </div>

    <Alert v-if="!!error" :msg="error.message" severity="error"></Alert>

    <p v-if="loading">
      Loading...
    </p>

    <img style="width: 100%" v-if="!loading && !error && !!imageBase64Data" v-bind:src="imageBase64Data" alt="Business model" id="model_img">
  </div>
</template>

<script>
import axios from "axios";
import Alert from "../generic/Alert";

export default {
  name: 'ChartContent',
  components: {Alert},
  data() {
    return {
      imageBase64Data: undefined,
      minNodeValue: 0,
      loading: false,
      error: null
    }
  },
  props: {
    fileData: File,
    columnsConfirmedString: String,
    backendConfirmedUrl: String,
  },
  methods: {
    fetchImage() {
      this.error = null;

      this.loading = true;
      var bodyFormdata = new FormData();
      bodyFormdata.append('file', this.fileData)
      bodyFormdata.append('columns', this.columnsConfirmedString)
      bodyFormdata.append('tsh', this.minNodeValue ? this.minNodeValue : 0)

      axios
          .post(`http://localhost:5000/generate`, bodyFormdata,
              {responseType: 'arraybuffer'}
          )
          .then(response => {
            let returnedB64 = Buffer.from(response.data).toString('base64');
            this.imageBase64Data = `data:image/png;base64, ${returnedB64}`;
          })
          .catch(err => {
            this.error = err;
          })
          .finally(() => {
            this.loading = false;
          })
    }

  },
  mounted() {
    this.fetchImage();
  },
  watch: {
    minNodeValue: function () {
      this.fetchImage();
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

#model_img {
  margin-left: auto;
  margin-right: auto;
  display: block;
}
</style>
