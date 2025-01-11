import { defineComponent as c, computed as p, ref as d, onMounted as m, nextTick as f, onUnmounted as v, watch as _, openBlock as b, createElementBlock as x } from "vue";
import { BulletLegend as u } from "@unovis/ts";
import { useForwardProps as g, arePropsEqual as k } from "../../utils/props.js";
const P = u.selectors, S = /* @__PURE__ */ c({
  __name: "index",
  props: {
    items: {},
    labelClassName: {},
    onLegendItemClick: { type: Function },
    labelFontSize: {},
    labelMaxWidth: {},
    bulletSize: {},
    bulletShape: {},
    orientation: {},
    renderIntoProvidedDomNode: { type: Boolean },
    data: {}
  },
  setup(s, { expose: i }) {
    const l = s;
    p(() => l.data);
    const t = g(l), o = d(), n = d();
    return m(() => {
      f(() => {
        n.value && (o.value = new u(n.value, { ...t.value, renderIntoProvidedDomNode: !0 }));
      });
    }), v(() => {
      var e;
      (e = o.value) == null || e.destroy();
    }), _(t, (e, a) => {
      var r;
      k(e, a) || (r = o.value) == null || r.update(t.value);
    }), i({
      component: o
    }), (e, a) => (b(), x("div", {
      "data-vis-bullet-legend": "",
      ref_key: "elRef",
      ref: n
    }, null, 512));
  }
});
export {
  P as VisBulletLegendSelectors,
  S as default
};
//# sourceMappingURL=index.js.map
