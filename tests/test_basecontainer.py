import pytest
from tests.testutils import make_concrete

import gc

import pygment


BaseComponent = make_concrete(pygment.component.BaseComponent)
BaseContainer = make_concrete(pygment.component.BaseContainer)


@pytest.fixture
def component(): return BaseComponent("dummy_component", (0,0,0,0))


@pytest.fixture
def container(): return BaseContainer("dummy_container", (0,0,0,0))




def test_container_add(container: BaseContainer, component: BaseComponent):
    container.add(component)
    
    assert component in container.elements.values()
    assert component.name in container.elements
    assert container is component.parent
    
    
def test_component_join(container: BaseContainer, component: BaseComponent):
    component.join(container)
    
    assert component in container.elements.values()
    assert component.name in container.elements
    assert container is component.parent
    
    
def test_container_add_raises_on_name_conflict(container: BaseContainer, component: BaseComponent):
    container.add(component)
    
    component1 = BaseComponent("dummy_component", (0,0,0,0))
    with pytest.raises(ValueError):
        container.add(component1)
        
        
def test_container_add_raises_on_parent_conflict(container: BaseContainer, component: BaseComponent):
    container.add(component)
    
    container1 = BaseContainer("dummy_container1", (0,0,0,0))
    with pytest.raises(ValueError):
        container1.add(component)
        
        
def test_container_getattr_name_lookup(container: BaseContainer, component: BaseComponent):
    container.add(component)
    compname = component.name
    
    assert hasattr(container, compname)
    assert getattr(container, compname) is component
    
    
def test_component_del_leaves_container_unchanged(container: BaseContainer, component: BaseComponent):
    container.add(component)
    compname = component.name
    assert compname in container.elements
    
    del component
    gc.collect()
    assert compname in container.elements
    
    
def test_container_del_kills_component_parent(component: BaseComponent):
    container = BaseContainer("dummy_container", (0,0,0,0))
    container.add(component)
    assert component.parent is not None
    
    del container
    gc.collect()
    assert component.parent is None
