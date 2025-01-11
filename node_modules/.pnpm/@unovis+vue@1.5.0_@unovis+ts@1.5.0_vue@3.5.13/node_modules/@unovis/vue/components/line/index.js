import { defineComponent as d, inject as m, computed as v, ref as f, onMounted as y, nextTick as h, onUnmounted as x, watch as l, openBlock as _, createElementBlock as F } from "vue";
import { Line as i } from "@unovis/ts";
import { useForwardProps as b, arePropsEqual as g } from "../../utils/props.js";
import { componentAccessorKey as k } from "../../utils/context.js";
const B = { "data-vis-component": "" }, O = i.selectors, S = /* @__PURE__ */ d({
  __name: "index",
  props: {
    color: {},
    curveType: {},
    lineWidth: {},
    lineDashArray: {},
    fallbackValue: {},
    highlightOnHover: { type: Boolean },
    cursor: {},
    x: {},
    y: {},
    id: { type: Function },
    xScale: { type: [Object, Function] },
    yScale: { type: [Object, Function] },
    excludeFromDomainCalculation: { type: Boolean },
    duration: {},
    events: {},
    attributes: {},
    data: {}
  },
  setup(u, { expose: p }) {
    const o = m(k), c = u, a = v(() => o.data.value ?? c.data), n = b(c), t = f();
    return y(() => {
      h(() => {
        var e;
        t.value = new i(n.value), (e = t.value) == null || e.setData(a.value), o.update(t.value);
      });
    }), x(() => {
      var e;
      (e = t.value) == null || e.destroy(), o.destroy();
    }), l(n, (e, r) => {
      var s;
      g(e, r) || (s = t.value) == null || s.setConfig(n.value);
    }), l(a, () => {
      var e;
      (e = t.value) == null || e.setData(a.value);
    }), p({
      component: t
    }), (e, r) => (_(), F("div", B));
  }
});
export {
  O as VisLineSelectors,
  S as default
};
//# sourceMappingURL=index.js.map
