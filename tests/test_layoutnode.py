import pytest
from tests.testutils import make_concrete

import gc

import pygment.core.layoutnode as layoutnode
LayoutNode = make_concrete(layoutnode.LayoutNode)


@pytest.fixture
def component(): return LayoutNode("dummy_component", (0,0,0,0))


@pytest.fixture
def container(): return LayoutNode("dummy_container", (0,0,0,0))




def test_container_add(container, component):
    container.add(component)
    
    assert component in container.children
    assert container is component.parent
    
    
def test_component_join(container, component):
    component.join(container)
    
    assert component in container.children
    assert container is component.parent
    
    
def test_container_add_raises_on_name_conflict(container, component):
    container.add(component)
    
    component1 = LayoutNode("dummy_component", (0,0,0,0))
    with pytest.raises(ValueError):
        container.add(component1)
        
        
def test_container_add_raises_on_parent_conflict(container, component):
    container.add(component)
    
    container1 = LayoutNode("dummy_container1", (0,0,0,0))
    with pytest.raises(ValueError):
        container1.add(component)
        
        
def test_container_getattr_name_lookup(container, component):
    container.add(component)
    compname = component.name
    
    assert hasattr(container, compname)
    assert getattr(container, compname) is component
    
    
def test_component_del_leaves_container_unchanged(container):
    component = LayoutNode("dummy_component", (0,0,0,0))
    assert not container.children
    
    container.add(component)
    assert component in container.children
    
    del component
    gc.collect()
    assert container.children
    
    
def test_container_del_kills_component_parent(component):
    container = LayoutNode("dummy_container", (0,0,0,0))
    container.add(component)
    assert component.parent is not None
    
    del container
    gc.collect()
    assert component.parent is None
