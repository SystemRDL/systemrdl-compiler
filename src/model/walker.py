
from ..model import component as comp
from .context import RDLContext

#===============================================================================
class RDLListener:
    
    def enter_Component_before(self, ctx:RDLContext):
        pass
    
    def enter_Component_after(self, ctx:RDLContext):
        pass
        
    def exit_Component_before(self, ctx:RDLContext):
        pass
        
    def exit_Component_after(self, ctx:RDLContext):
        pass
    
    def enter_Addrmap(self, ctx:RDLContext):
        pass
    
    def exit_Addrmap(self, ctx:RDLContext):
        pass
    
    def enter_Regfile(self, ctx:RDLContext):
        pass
    
    def exit_Regfile(self, ctx:RDLContext):
        pass
    
    def enter_Mem(self, ctx:RDLContext):
        pass
    
    def exit_Mem(self, ctx:RDLContext):
        pass
    
    def enter_Reg(self, ctx:RDLContext):
        pass
    
    def exit_Reg(self, ctx:RDLContext):
        pass
    
    def enter_Field(self, ctx:RDLContext):
        pass
    
    def exit_Field(self, ctx:RDLContext):
        pass
    
    def enter_Signal(self, ctx:RDLContext):
        pass
    
    def exit_Signal(self, ctx:RDLContext):
        pass

#===============================================================================
class RDLWalker:
    
    def walk(self, listener:RDLListener, inst:comp.Inst, parent_ctx:RDLContext=None):
        
        ctx = RDLContext(inst, parent_ctx)
        
        self.do_enter(listener, ctx)
        for child in inst.typ.children:
            self.walk(listener, child, ctx)
        self.do_exit(listener, ctx)
    
    def do_enter(self, listener:RDLListener, ctx:RDLContext):
        listener.enter_Component_before(ctx)
        
        if(type(ctx.inst.typ) == comp.Addrmap):
            listener.enter_Addrmap(ctx)
        elif(type(ctx.inst.typ) == comp.Regfile):
            listener.enter_Regfile(ctx)
        elif(type(ctx.inst.typ) == comp.Mem):
            listener.enter_Mem(ctx)
        elif(type(ctx.inst.typ) == comp.Reg):
            listener.enter_Reg(ctx)
        elif(type(ctx.inst.typ) == comp.Field):
            listener.enter_Field(ctx)
        elif(type(ctx.inst.typ) == comp.Signal):
            listener.enter_Signal(ctx)
        
        listener.enter_Component_after(ctx)
        
    def do_exit(self, listener:RDLListener, ctx:RDLContext):
        listener.exit_Component_before(ctx)
        
        if(type(ctx.inst.typ) == comp.Addrmap):
            listener.exit_Addrmap(ctx)
        elif(type(ctx.inst.typ) == comp.Regfile):
            listener.exit_Regfile(ctx)
        elif(type(ctx.inst.typ) == comp.Mem):
            listener.exit_Mem(ctx)
        elif(type(ctx.inst.typ) == comp.Reg):
            listener.exit_Reg(ctx)
        elif(type(ctx.inst.typ) == comp.Field):
            listener.exit_Field(ctx)
        elif(type(ctx.inst.typ) == comp.Signal):
            listener.exit_Signal(ctx)
        
        listener.exit_Component_after(ctx)
