import Vue from 'https://cdn.jsdelivr.net/npm/vue@2.6.11/dist/vue.esm.browser.js'


Vue.component('loader', {
  template: `
    <div style="display: flex;justify-content: center;align-items: center">
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>
  `
})

new Vue({
  el: '#app',
  data() {
    return {
      form: {
        x: '4',
        y: '3',
        z: '2',
        vx: '4',
        vy: '3',
        vz: '1',
        tstart: '9',
        dt: '2',
        tend: '1'
      }
    }
  },
  methods: {
    async createContact() {
      const handledValues = await request('/api/contacts', 'POST', this.form)
      console.log('Sending data: ', this.form)
      console.log(JSON.parse(handledValues))
    }
  },

  async mounted() {
    let serverData = await request('/api/contacts')
    console.log(serverData)
    this.form = serverData
  }
})

async function request(url, method = 'GET', data = null) {
  try {
    const headers = {}
    let body

    if (data) {
      headers['Content-Type'] = 'application/json'
      body = JSON.stringify(data)
    }

    const response = await fetch(url, {
      method,
      headers,
      body
    })
    return await response.json()
  } catch (e) {
    console.warn('Error:', e.message)
  }
}
