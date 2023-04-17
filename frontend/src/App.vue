<template>
  <v-card>
      <v-layout>
          <Navigation/>
      </v-layout>
  </v-card>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import Navigation from "@/components/Navigation.vue";
export default {
  name: 'App',
  components: {
      Navigation,
      // eslint-disable-next-line vue/no-unused-components
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
