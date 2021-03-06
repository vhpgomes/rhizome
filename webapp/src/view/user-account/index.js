
import Vue from 'vue'
import _ from 'lodash'
import api from '../../data/api'
import treeify from '../../data/transform/treeify'
import ancestoryString from '../../data/transform/ancestryString'
import MenuVue from '../../component/vue-menu'

export default {
  template: require('./template.html'),
  data: function () {
    return {
      locations: [],
      groups: []
    }
  },
  created: function () {
    var self = this
    self.$set('locationalAccessLoading', true)
    var MenuComponent = Vue.extend(MenuVue)

    api.groups().then(function (response) {
      var groups = response.objects
      api.user_permissions({'user_id': self.$parent.$data.user_id}, null, {'cache-control': 'no-cache'}).then(function (data) {
        _.forEach(groups, function (group) {
          group.active = _.some(data.objects, {'group_id': group.id})
        })
        self.$set('groups', response.objects)
      })
    })

    api.locations().then(function (items) {
      self.loadlocationalAccess()
      self.location_map = _.indexBy(items.objects, 'id')
      var locations = _(items.objects)
        .map(function (location) {
          return {
            'title': location.name,
            'value': location.id,
            'id': location.id,
            'parent': location.parent_location_id
          }
        })
        .sortBy('title')
        .reverse() // I do not know why this works, but it does
        .thru(_.curryRight(treeify)('id'))
        .thru(ancestoryString)
        .value()
      self.$set('locations', locations)
    }).then(function () {
      self.locationMenu = new MenuComponent({
        el: '#locations'
      })
      self.locationMenu.items = self.$data.locations
      self.locationMenu.$on('field-selected', self.addlocationalAccess)
    })
  },
  methods: {
    addRemoveUserGroup: function (e) {
      var groupId = e.target.getAttribute('data-group-id')
      if (e.target.checked) {
        api.post_user_permission({'user_id': this.$parent.$data.user_id, 'group_id': groupId})
      } else {
        api.delete_user_permission({'user_id': this.$parent.$data.user_id, 'group_id': groupId})
      }
    },
    addlocationalAccess: function (data) {
      var self = this
      self.$set('locationalAccessLoading', true)
      api.set_location_responsibility({ user_id: this.$parent.$data.user_id, location_id: data }).then(function () {
        self.loadlocationalAccess()
      })
    },
    deletelocationalAccess: function (data) {
      var self = this
      api.delete_location_responsibility({ id: data }).then(function () {
        self.loadlocationalAccess()
      })
    },
    loadlocationalAccess: function () {
      var self = this

      api.location_responsibility({ user_id: this.$parent.$data.user_id }, null, {'cache-control': 'no-cache'}).then(function (data) {
        var locations = data.objects
        _.forEach(locations, function (location) {
          location.name = self.location_map[location.location_id].name
        })
        self.$set('location_responsibilities', locations)
        self.$set('locationalAccessLoading', false)
      })
    }
  }
}
