#!/usr/bin/env python
# coding: utf-8
# controller module

from config import debug
import datamodel as m
import view as v
from bokeh.events import Tap
import sys


dontplot = False

def click_frontal_callback(event):
    if debug: print("Called click_frontal_callback().")
    global dontplot #helper variable to not plot the same image twice

    #normalising click coords
    if event.x<1:
        x = 1
    elif event.x > v.slice_slider_sagittal.end:
        x = slice_slider_sagittal.end
    else:
        x = int(event.x)

    if event.y<1:
        y = 1
    elif event.y > v.slice_slider_axial.end:
        y = v.slice_slider_axial.end
    else:
        y = int(event.y)

    dontplot = True
    v.slice_slider_sagittal.update(value = x)
    dontplot = False
    v.slice_slider_axial.update(value = y)
    if not v.toggle_regions.active: v.plot_sagittal()

def click_axial_callback(event):
    if debug: print("Called click_axial_callback().")
    global dontplot

    #normalising click coords
    if event.x<1:
        x = 1
    elif event.x > v.slice_slider_sagittal.end:
        x = v.slice_slider_sagittal.end
    else:
        x = int(event.x)

    if event.y<1:
        y = 1
    elif event.y > v.slice_slider_frontal.end:
        y = v.slice_slider_frontal.end
    else:
        y = int(event.y)

    dontplot = True
    v.slice_slider_frontal.update(value = v.slice_slider_frontal.end - y+1)
    dontplot = False
    v.slice_slider_sagittal.update(value = x)
    if not v.toggle_regions.active: v.plot_frontal()

def click_sagittal_callback(event):
    if debug: print("Called click_sagittal_callback().")
    global dontplot

    #normalising click coords
    if event.x<1:
        x = 1
    elif event.x > v.slice_slider_frontal.end:
        x = v.slice_slider_frontal.end
    else:
        x = int(event.x)

    if event.y<1:
        y = 1
    elif event.y > v.slice_slider_axial.end:
        y = v.slice_slider_axial.end
    else:
        y = int(event.y)

    dontplot = True
    v.slice_slider_frontal.update(value = x)
    dontplot = False
    v.slice_slider_axial.update(value = y)
    if not v.toggle_regions.active: v.plot_frontal()



v.p_frontal.on_event(Tap, click_frontal_callback)
v.p_axial.on_event(Tap, click_axial_callback)
v.p_sagittal.on_event(Tap, click_sagittal_callback)



# for jupyter notebook:
#show(layout)
# alternatively, add layout to the document (for bokeh server)
v.curdoc().add_root(v.layout)
v.curdoc().title = 'Online AD brain viewer'



def select_subject_callback(attr, old, new):
    if debug: print("Called select_subject_callback().")
    v.disable_widgets()
    
    m.set_subject( m.index_lst[m.sorted_xs.index(v.subject_select.value)] ) #this parameter is subj_id
    
    v.update_subject_divs(m.index_lst[m.sorted_xs.index(v.subject_select.value)]) #called with subj_id; corresponding RID/sid would be m.grps.iloc[m.index_lst[m.sorted_xs.index(v.subject_select.value)], 1]

    v.p_frontal.title.text = "Scan predicted as %0.2f%% Alzheimer\'s" % m.pred
    v.p_axial.title.text = " "
    v.p_sagittal.title.text = " "
    v.apply_thresholds(m.relevance_map, threshold = v.threshold_slider.value, cluster_size = v.clustersize_slider.value)

    v.update_guide_frontal()
    v.update_guide_axial()
    v.update_guide_sagittal()

    v.plot_frontal()
    v.plot_axial()
    v.plot_sagittal()
    v.update_cluster_divs()
    v.enable_widgets()



def select_model_callback(attr, old, new):
    v.disable_widgets()
    v.curdoc().hold()

    print("Called select_model_callback().")
    m.set_model(v.model_select.value)
    select_subject_callback('','','')

    v.curdoc().unhold()
    print("Finished selecting new model.")
    v.enable_widgets()


def apply_thresholds_callback(attr, old, new):
    if debug: print("Called apply_thresholds_callback().")
    v.apply_thresholds(m.relevance_map, threshold = v.threshold_slider.value, cluster_size = v.clustersize_slider.value)
    v.update_guide_frontal()
    v.update_guide_axial()
    v.update_guide_sagittal()
    v.update_cluster_divs()
    v.plot_frontal()
    v.plot_axial()
    v.plot_sagittal()

def set_slice_frontal_callback(attr, old, new):
    if debug: print("Called set_slice_frontal_callback().")

    v.axial_crosshair_from_frontal.update(location = v.slice_slider_frontal.end - new +1)
    v.sagittal_crosshair_from_frontal.update(location = new -1)
    v.update_region_div()
    v.update_cluster_divs()
    if not dontplot: #is set True if called from crosshair-click-callback
        v.plot_frontal()
    if v.toggle_regions.active and not dontplot:
        v.plot_axial()
        v.plot_sagittal()

def set_slice_axial_callback(attr, old, new):
    if debug: print("Called set_slice_axial_callback().")

    v.frontal_crosshair_from_axial.update(location =  new -1)
    v.sagittal_crosshair_from_axial.update(location = new -1)
    v.update_region_div()
    v.update_cluster_divs()
    if not dontplot:
        v.plot_axial()
    if v.toggle_regions.active and not dontplot:
        v.plot_frontal()
        v.plot_sagittal()

def set_slice_sagittal_callback(attr, old, new):
    if debug: print("Called set_slice_sagittal_callback().")

    v.frontal_crosshair_from_sagittal.update(location=(new -1))
    v.axial_crosshair_from_sagittal.update(location=(new -1))
    v.update_region_div()
    v.update_cluster_divs()
    if not dontplot:
        v.plot_sagittal()
    if v.toggle_regions.active and not dontplot:
        v.plot_frontal()
        v.plot_axial()

def set_transparency_callback(attr, old, new):
    v.plot_frontal()
    v.plot_axial()
    v.plot_sagittal()

def click_show_regions_callback(attr):
    if(v.toggle_regions.active):
        v.plot_frontal_region()
        v.plot_axial_region()
        v.plot_sagittal_region()
    else:
        v.plot_frontal()
        v.plot_axial()
        v.plot_sagittal()

v.toggle_regions.on_click(click_show_regions_callback)
v.subject_select.on_change('value', select_subject_callback)

v.curdoc().hold()
select_subject_callback('','','') # call once
v.curdoc().unhold()
v.firstrun = False

v.slice_slider_frontal.on_change('value', set_slice_frontal_callback)
v.slice_slider_axial.on_change('value', set_slice_axial_callback)
v.slice_slider_sagittal.on_change('value', set_slice_sagittal_callback)
v.threshold_slider.on_change('value', apply_thresholds_callback)
v.clustersize_slider.on_change('value', apply_thresholds_callback)
v.transparency_slider.on_change('value', set_transparency_callback)

v.model_select.on_change('value', select_model_callback)

# In[19]:

v.subject_select.value=m.sorted_xs[0]

# automatically close bokeh after browser window was closed
#def close_session(session_context):
#    sys.exit()  # Stop the server
#v.curdoc().on_session_destroyed(close_session)