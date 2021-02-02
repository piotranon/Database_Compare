<template>
  <div class="home">
    <mainView />
  </div>
</template>

<script>
// @ is an alias to /src
import mainView from "@/components/mainView.vue";

export default {
  name: "Home",
  components: {
    mainView
  }
};
</script>
