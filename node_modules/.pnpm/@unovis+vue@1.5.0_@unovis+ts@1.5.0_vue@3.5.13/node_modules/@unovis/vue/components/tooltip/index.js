import { defineComponent as i, inject as p, ref as m, onMounted as u, nextTick as f, onUnmounted as d, watch as v, openBlock as _, createElementBlock as h } from "vue";
import { Tooltip as a } from "@unovis/ts";
import { useForwardProps as w, arePropsEqual as x } from "../../utils/props.js";
import { tooltipAccessorKey as y } from "../../utils/context.js";
const g = { "data-vis-tooltip": "" }, T = a.selectors, z = /* @__PURE__ */ i({
  __name: "index",
  props: {
    components: {},
    container: {},
    followCursor: { type: Boolean },
    allowHover: { type: Boolean },
    horizontalPlacement: {},
    horizontalShift: {},
    verticalPlacement: {},
    verticalShift: {},
    triggers: {},
    attributes: {},
    className: {},
    data: {}
  },
  setup(c, { expose: l }) {
    const r = p(y), t = w(c), o = m();
    return u(() => {
      f(() => {
        o.value = new a(t.value), r.update(o.value);
      });
    }), d(() => {
      var e;
      (e = o.value) == null || e.destroy(), r.destroy();
    }), v(t, (e, n) => {
      var s;
      x(e, n) || (s = o.value) == null || s.setConfig(t.value);
    }), l({
      component: o
    }), (e, n) => (_(), h("div", g));
  }
});
export {
  T as VisTooltipSelectors,
  z as default
};
//# sourceMappingURL=index.js.map
