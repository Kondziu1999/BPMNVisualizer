<template>
  <div v-bind:class="{
    'alert': true,
    'success': (severity==='success'),
    'warning': (severity==='warning'),
    'error':(severity==='error')
  }">
    <p>
      {{ msg }}
    </p>

    <v-icon v-if="severity==='success'">
      mdi-check
    </v-icon>
    <v-icon v-if="severity==='warning'">
      mdi-alert
    </v-icon>
    <v-icon v-if="severity==='error'">
      mdi-alert-octagon
    </v-icon>
  </div>
</template>

<script>
export default {
  name: "Alert",
  props: {
    msg: String,
    severity: String
  }
}
</script>

<style scoped>
.alert {
  border-width: 2px;
  color: white;
  border-style: solid;
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 500px;
  padding: 10px;
}
.success {
  background-color: #4caf50;
}

.success v-icon {
  color: #4caf50;
}

.warning {
  background-color: #fb8c00;
}

.warning v-icon {
  color: #fb8c00;
}

.error {
  background-color: #ff5252;
}

.error v-icon {
  color: #ff5252;
}

</style>