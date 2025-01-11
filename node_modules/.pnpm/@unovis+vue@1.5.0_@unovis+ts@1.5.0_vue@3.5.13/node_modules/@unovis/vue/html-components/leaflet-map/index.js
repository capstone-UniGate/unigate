import { defineComponent as d, computed as f, ref as p, onMounted as m, nextTick as y, onUnmounted as v, watch as M, openBlock as L, createElementBlock as B } from "vue";
import { LeafletMap as r } from "@unovis/ts";
import { useForwardProps as b, arePropsEqual as g } from "../../utils/props.js";
const F = r.selectors, w = /* @__PURE__ */ d({
  __name: "index",
  props: {
    width: {},
    height: {},
    flyToDuration: {},
    fitViewPadding: {},
    zoomDuration: {},
    initialBounds: {},
    fitBoundsOnUpdate: {},
    fitViewOnInit: { type: Boolean },
    fitViewOnUpdate: { type: Boolean },
    style: {},
    styleDarkTheme: {},
    accessToken: {},
    attribution: {},
    renderer: {},
    onMapInitialized: { type: Function },
    onMapMoveZoom: { type: Function },
    onMapMoveStart: { type: Function },
    onMapMoveEnd: { type: Function },
    onMapZoomStart: { type: Function },
    onMapZoomEnd: { type: Function },
    onMapClick: { type: Function },
    pointLongitude: {},
    pointLatitude: {},
    pointId: {},
    pointShape: {},
    pointColor: {},
    pointRadius: {},
    pointLabel: {},
    pointLabelColor: {},
    pointBottomLabel: {},
    pointCursor: {},
    pointRingWidth: {},
    selectedPointId: {},
    clusterColor: {},
    clusterRadius: {},
    clusterLabel: {},
    clusterLabelColor: {},
    clusterBottomLabel: {},
    clusterRingWidth: {},
    clusterBackground: { type: Boolean },
    clusterExpandOnClick: { type: Boolean },
    clusteringDistance: {},
    colorMap: {},
    topoJSONLayer: {},
    tooltip: {},
    ariaLabel: {},
    duration: {},
    events: {},
    attributes: {},
    data: {}
  },
  setup(u, { expose: c }) {
    const a = u, s = f(() => a.data), o = b(a), e = p(), n = p();
    return m(() => {
      y(() => {
        n.value && (e.value = new r(n.value, o.value, s.value));
      });
    }), v(() => {
      var t;
      (t = e.value) == null || t.destroy();
    }), M(o, (t, i) => {
      var l;
      g(t, i) || (l = e.value) == null || l.setConfig(o.value);
    }), c({
      component: e
    }), (t, i) => (L(), B("div", {
      "data-vis-leaflet-map": "",
      ref_key: "elRef",
      ref: n
    }, null, 512));
  }
});
export {
  F as VisLeafletMapSelectors,
  w as default
};
//# sourceMappingURL=index.js.map
