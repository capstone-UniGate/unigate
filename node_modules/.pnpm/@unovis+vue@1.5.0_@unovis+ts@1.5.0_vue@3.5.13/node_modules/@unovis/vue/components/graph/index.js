import { defineComponent as p, inject as y, computed as m, ref as S, onMounted as F, nextTick as b, onUnmounted as k, watch as r, openBlock as g, createElementBlock as h } from "vue";
import { Graph as u } from "@unovis/ts";
import { useForwardProps as L, arePropsEqual as v } from "../../utils/props.js";
import { componentAccessorKey as f } from "../../utils/context.js";
const C = { "data-vis-component": "" }, G = u.selectors, D = /* @__PURE__ */ p({
  __name: "index",
  props: {
    zoomScaleExtent: {},
    disableZoom: { type: Boolean },
    zoomEventFilter: { type: Function },
    disableDrag: { type: Boolean },
    disableBrush: { type: Boolean },
    zoomThrottledUpdateNodeThreshold: {},
    layoutType: {},
    layoutAutofit: { type: Boolean },
    layoutAutofitTolerance: {},
    layoutNonConnectedAside: { type: Boolean },
    layoutNodeGroup: {},
    layoutGroupOrder: {},
    layoutParallelNodesPerColumn: {},
    layoutParallelNodeSubGroup: {},
    layoutParallelSubGroupsPerRow: {},
    layoutParallelGroupSpacing: {},
    layoutParallelSortConnectionsByGroup: {},
    forceLayoutSettings: {},
    dagreLayoutSettings: {},
    layoutElkSettings: {},
    layoutElkNodeGroups: {},
    linkWidth: {},
    linkStyle: {},
    linkBandWidth: {},
    linkArrow: {},
    linkStroke: {},
    linkDisabled: {},
    linkFlow: {},
    linkFlowAnimDuration: {},
    linkFlowParticleSize: {},
    linkLabel: {},
    linkLabelShiftFromCenter: {},
    linkNeighborSpacing: {},
    linkCurvature: {},
    selectedLinkId: {},
    nodeSize: {},
    nodeStrokeWidth: {},
    nodeShape: {},
    nodeGaugeValue: {},
    nodeGaugeFill: {},
    nodeGaugeAnimDuration: {},
    nodeIcon: {},
    nodeIconSize: {},
    nodeLabel: {},
    nodeLabelTrim: {},
    nodeLabelTrimMode: {},
    nodeLabelTrimLength: {},
    nodeSubLabel: {},
    nodeSubLabelTrim: {},
    nodeSubLabelTrimMode: {},
    nodeSubLabelTrimLength: {},
    nodeSideLabels: {},
    nodeBottomIcon: {},
    nodeDisabled: {},
    nodeFill: {},
    nodeStroke: {},
    nodeSort: { type: Function },
    nodeEnterPosition: {},
    nodeEnterScale: {},
    nodeExitPosition: {},
    nodeExitScale: {},
    nodeEnterCustomRenderFunction: { type: Function },
    nodeUpdateCustomRenderFunction: { type: Function },
    nodePartialUpdateCustomRenderFunction: { type: Function },
    nodeExitCustomRenderFunction: { type: Function },
    nodeOnZoomCustomRenderFunction: { type: Function },
    nodeSelectionHighlightMode: {},
    selectedNodeId: {},
    selectedNodeIds: {},
    panels: {},
    onNodeDragStart: { type: Function },
    onNodeDrag: { type: Function },
    onNodeDragEnd: { type: Function },
    onZoom: { type: Function },
    onZoomStart: { type: Function },
    onZoomEnd: { type: Function },
    onLayoutCalculated: { type: Function },
    onNodeSelectionBrush: { type: Function },
    onNodeSelectionDrag: { type: Function },
    onRenderComplete: { type: Function },
    duration: {},
    events: {},
    attributes: {},
    data: {}
  },
  setup(c, { expose: s }) {
    const n = y(f), l = c, t = m(() => n.data.value ?? l.data), a = L(l), o = S();
    return F(() => {
      b(() => {
        var e;
        o.value = new u(a.value), (e = o.value) == null || e.setData(t.value), n.update(o.value);
      });
    }), k(() => {
      var e;
      (e = o.value) == null || e.destroy(), n.destroy();
    }), r(a, (e, i) => {
      var d;
      v(e, i) || (d = o.value) == null || d.setConfig(a.value);
    }), r(t, () => {
      var e;
      (e = o.value) == null || e.setData(t.value);
    }), s({
      component: o
    }), (e, i) => (g(), h("div", C));
  }
});
export {
  G as VisGraphSelectors,
  D as default
};
//# sourceMappingURL=index.js.map
