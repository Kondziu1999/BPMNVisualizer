<template>
  <div id="leftPanel">
    <h1 class="title">
      BPMN visualizer
    </h1>

    <div v-for="element in sideBarElements"
         :key="element.value"
         @click="() => setRoute(element.value)"
         class="sideBarElement"
         v-bind:class="{'sideBarElement': true, 'sideBarElementActive': (route===element.value), 'sideBarElementInvalid': element.warning}">
      <h3>
        {{ element.primary }}
      </h3>
      <v-icon v-if="element.warning" color="white">
        mdi-alert
      </v-icon>
      <v-icon v-if="element.done" color="white">
        mdi-check
      </v-icon>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeftPanel',
  props: {
    backendConfirmed: Boolean,
    backendConfirmedUrl: String,
    fileConfirmed: Boolean,
    route: String
  },
  computed: {
    sideBarElements(){
      return [
        {
          primary: 'Konfiguracja środowiska',
          value: 'BACKEND',
          warning: false,
          done: this.backendConfirmed
        },
        {
          primary: 'Dane wejściowe',
          value: 'FILE',
          warning: !this.backendConfirmed,
          done: this.fileConfirmed,
        },
        {
          primary: 'Wizualizacja',
          value: 'CHART',
          warning: !this.fileConfirmed || !this.backendConfirmed,
          done: false,
        }
      ]
    }
  },
  data() {
    return {
    }
  },
  methods: {
    editBackend() {
      this.$emit('editBackend')
    },
    editFile() {
      this.$emit('editFile')
    },
    setRoute(newRoute) {
      this.$emit('setRoute', newRoute)
    }
  }
}
</script>

<style scoped>
  @import "../variables.css";

  #leftPanel {
    background-color: #34495E;
    color: white;
    height: 100%;
    width: 300px;
    position: sticky;
    z-index: 1;
    top: 0;
    left: 0;
  }

  .title {
    color: white;
    font-weight: 900;
    font-size: 40px;
    padding: var(--sindenav-padding);
    margin-bottom: 30px;
  }

  .sideBarElement {
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--sindenav-padding);
  }

  .sideBarElementActive {
    background-color: #fb8c00;
  }

  .sideBarElementInvalid {
    background-color: #cccccc;
    pointer-events: none;
  }

</style>
