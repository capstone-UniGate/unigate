import { defineComponent as d, computed as f, ref as r, onMounted as m, nextTick as y, onUnmounted as L, watch as M, openBlock as v, createElementBlock as w } from "vue";
import { LeafletFlowMap as u } from "@unovis/ts";
import { useForwardProps as g, arePropsEqual as F } from "../../utils/props.js";
const k = u.selectors, b = /* @__PURE__ */ d({
  __name: "index",
  props: {
    sourceLongitude: {},
    sourceLatitude: {},
    targetLongitude: {},
    targetLatitude: {},
    sourcePointRadius: {},
    sourcePointColor: {},
    flowParticleColor: {},
    flowParticleRadius: {},
    flowParticleSpeed: {},
    flowParticleDensity: {},
    onSourcePointClick: { type: Function },
    onSourcePointMouseEnter: { type: Function },
    onSourcePointMouseLeave: { type: Function },
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
  setup(c, { expose: p }) {
    const i = c, s = f(() => i.data), t = g(i), e = r(), n = r();
    return m(() => {
      y(() => {
        n.value && (e.value = new u(n.value, t.value, s.value));
      });
    }), L(() => {
      var o;
      (o = e.value) == null || o.destroy();
    }), M(t, (o, a) => {
      var l;
      F(o, a) || (l = e.value) == null || l.setConfig(t.value);
    }), p({
      component: e
    }), (o, a) => (v(), w("div", {
      "data-vis-leaflet-flow-map": "",
      ref_key: "elRef",
      ref: n
    }, null, 512));
  }
});
export {
  k as VisLeafletFlowMapSelectors,
  b as default
};
//# sourceMappingURL=index.js.map
