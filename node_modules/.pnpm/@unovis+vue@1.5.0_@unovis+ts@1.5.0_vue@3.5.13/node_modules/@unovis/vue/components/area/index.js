import { defineComponent as d, inject as m, computed as v, ref as y, onMounted as f, nextTick as x, onUnmounted as _, watch as u, openBlock as F, createElementBlock as b } from "vue";
import { Area as i } from "@unovis/ts";
import { useForwardProps as h, arePropsEqual as B } from "../../utils/props.js";
import { componentAccessorKey as g } from "../../utils/context.js";
const j = { "data-vis-component": "" }, D = i.selectors, P = /* @__PURE__ */ d({
  __name: "index",
  props: {
    color: {},
    curveType: {},
    baseline: {},
    opacity: {},
    cursor: {},
    minHeight1Px: { type: Boolean },
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
  setup(l, { expose: p }) {
    const o = m(g), c = l, a = v(() => o.data.value ?? c.data), n = h(c), t = y();
    return f(() => {
      x(() => {
        var e;
        t.value = new i(n.value), (e = t.value) == null || e.setData(a.value), o.update(t.value);
      });
    }), _(() => {
      var e;
      (e = t.value) == null || e.destroy(), o.destroy();
    }), u(n, (e, r) => {
      var s;
      B(e, r) || (s = t.value) == null || s.setConfig(n.value);
    }), u(a, () => {
      var e;
      (e = t.value) == null || e.setData(a.value);
    }), p({
      component: t
    }), (e, r) => (F(), b("div", j));
  }
});
export {
  D as VisAreaSelectors,
  P as default
};
//# sourceMappingURL=index.js.map
