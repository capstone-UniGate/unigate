import { defineComponent as i, inject as m, computed as v, ref as g, onMounted as f, nextTick as y, onUnmounted as _, watch as u, openBlock as b, createElementBlock as h } from "vue";
import { Donut as l } from "@unovis/ts";
import { useForwardProps as B, arePropsEqual as k } from "../../utils/props.js";
import { componentAccessorKey as w } from "../../utils/context.js";
const x = { "data-vis-component": "" }, E = l.selectors, L = /* @__PURE__ */ i({
  __name: "index",
  props: {
    id: { type: Function },
    value: {},
    angleRange: {},
    padAngle: {},
    sortFunction: { type: Function },
    cornerRadius: {},
    color: {},
    radius: {},
    arcWidth: {},
    centralLabel: {},
    centralSubLabel: {},
    centralSubLabelWrap: { type: Boolean },
    showEmptySegments: { type: Boolean },
    emptySegmentAngle: {},
    showBackground: { type: Boolean },
    backgroundAngleRange: {},
    duration: {},
    events: {},
    attributes: {},
    data: {}
  },
  setup(p, { expose: d }) {
    const o = m(w), r = p, n = v(() => o.data.value ?? r.data), a = B(r), t = g();
    return f(() => {
      y(() => {
        var e;
        t.value = new l(a.value), (e = t.value) == null || e.setData(n.value), o.update(t.value);
      });
    }), _(() => {
      var e;
      (e = t.value) == null || e.destroy(), o.destroy();
    }), u(a, (e, c) => {
      var s;
      k(e, c) || (s = t.value) == null || s.setConfig(a.value);
    }), u(n, () => {
      var e;
      (e = t.value) == null || e.setData(n.value);
    }), d({
      component: t
    }), (e, c) => (b(), h("div", x));
  }
});
export {
  E as VisDonutSelectors,
  L as default
};
//# sourceMappingURL=index.js.map
